# PyTorch Recipes & High-Performance Deep Learning Reference

Synthesized from **PyTorch Official Recipes Index, Tutorials & Performance Standards**.

---

## 1. Automatic Mixed Precision (AMP) Internals
Mixed precision computes activations and weights in `float16` or `bfloat16` while preserving critical reductions in `float32`. This doubles throughput and reduces GPU VRAM consumption by up to $50\%$.

### Canonical AMP Training Step
```python
import torch

scaler = torch.amp.GradScaler("cuda", enabled=torch.cuda.is_available())

for data, target in dataloader:
    data = data.to("cuda", non_blocking=True)
    target = target.to("cuda", non_blocking=True)
    
    # Zero gradients with set_to_none=True to avoid zeroing memory buffers
    optimizer.zero_grad(set_to_none=True)
    
    with torch.amp.autocast("cuda", dtype=torch.bfloat16):
        output = model(data)
        loss = criterion(output, target)
        
    # Scale loss to prevent underflow in FP16 gradients
    scaler.scale(loss).backward()
    
    # Unscale before gradient clipping
    scaler.unscale_(optimizer)
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    
    scaler.step(optimizer)
    scaler.update()
```

*Note on `bfloat16` vs `float16`:*
- `bfloat16` has the same dynamic range as `float32` (8 exponent bits). Loss scaling is often unnecessary for `bfloat16`, whereas `float16` strictly requires `GradScaler`.

---

## 2. High-Throughput DataLoader Pipeline
DataLoaders are frequently the primary bottleneck in deep learning pipelines:
```python
dataloader = DataLoader(
    dataset,
    batch_size=128,
    shuffle=True,
    num_workers=4,               # 2-4 workers per GPU
    pin_memory=True,             # Direct DMA copy into page-locked host memory
    persistent_workers=True,     # Prevents worker teardown/recreation overhead between epochs
    prefetch_factor=2,           # Prefetches 2 batches per worker
)
```

---

## 3. Distributed Training Architecture (`torchrun` & DDP)

### Canonical Distributed Multi-GPU Blueprint
Launch using PyTorch's official runner:
```bash
torchrun --nproc_per_node=4 train_distributed.py
```

Implementation script (`train_distributed.py`):
```python
import os
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler

def setup_ddp():
    # torchrun automatically supplies RANK, LOCAL_RANK, and WORLD_SIZE
    dist.init_process_group(backend="nccl")
    local_rank = int(os.environ["LOCAL_RANK"])
    torch.cuda.set_device(local_rank)
    return local_rank

def cleanup_ddp():
    dist.destroy_process_group()

def main():
    local_rank = setup_ddp()
    
    # Model placement and DDP wrap
    model = MyDeepNet().to(local_rank)
    ddp_model = DDP(model, device_ids=[local_rank])
    
    # Distributed Sampler to shard dataset cleanly across GPUs without duplication
    sampler = DistributedSampler(dataset, shuffle=True)
    dataloader = DataLoader(dataset, batch_size=32, sampler=sampler, num_workers=2, pin_memory=True)
    
    for epoch in range(epochs):
        sampler.set_epoch(epoch)  # Crucial: ensures distinct shuffling per epoch
        for data, targets in dataloader:
            data, targets = data.to(local_rank), targets.to(local_rank)
            optimizer.zero_grad(set_to_none=True)
            loss = criterion(ddp_model(data), targets)
            loss.backward()
            optimizer.step()
            
    cleanup_ddp()
```

- **Fully Sharded Data Parallel (FSDP)**:
  - Shards model parameters, gradients, and optimizer states across multiple GPUs (ZeRO Stage 3).
  - Allows training multi-billion parameter models that exceed the memory of a single GPU.

---

## 4. PyTorch Profiler & Performance Optimization
Diagnose GPU starvation and CPU bottlenecks:
```python
with torch.profiler.profile(
    activities=[
        torch.profiler.ProfilerActivity.CPU,
        torch.profiler.ProfilerActivity.CUDA,
    ],
    schedule=torch.profiler.schedule(wait=1, warmup=1, active=3, repeat=1),
    on_trace_ready=torch.profiler.tensorboard_trace_handler("./log/profiler"),
    record_shapes=True,
    profile_memory=True,
    with_stack=True,
) as prof:
    for step, batch in enumerate(dataloader):
        train_step(batch)
        prof.step()
```

### PyTorch 2.0 `torch.compile`
Accelerate inference and training with fused Triton kernels:
```python
compiled_model = torch.compile(model, mode="reduce-overhead")
```
