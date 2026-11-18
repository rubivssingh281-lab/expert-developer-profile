# Reinforcement Learning with Verifiable Rewards (RLVR), GRPO & Production vLLM FP8 Serving

Authoritative engineering manual for training reasoning models with Group Relative Policy Optimization (GRPO), low-VRAM QLoRA reward verification, and ultra-high-throughput vLLM serving with FP8 dynamic quantization.

---

## 1. Group Relative Policy Optimization (GRPO)

Traditional Proximal Policy Optimization (PPO) requires maintaining both an Actor (Policy) network and an independent Critic (Value) network, doubling the parameter VRAM footprint. **GRPO** eliminates the critic network entirely by evaluating groups of $G$ sampled completions per prompt and calculating relative advantage:

```math
\mathcal{J}_{\text{GRPO}}(\theta) = \mathbb{E}_{q, \{o_i\}_{i=1}^G} \left[ \frac{1}{G} \sum_{i=1}^G \left( \min\left( r_i(\theta) \hat{A}_i, \text{clip}(r_i(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_i \right) - \beta \mathbb{D}_{\text{KL}}(\pi_\theta \| \pi_{\text{ref}}) \right) \right]
```

Where normalized relative advantage across the group $G$ is:

```math
\hat{A}_i = \frac{R(q, o_i) - \text{mean}(\{R(q, o_j)\})}{\text{std}(\{R(q, o_j)\}) + \varepsilon}
```

### Deterministic Verifiable Reward Functions
Reasoning tasks employ deterministic code-execution and math verification functions:

```python
from __future__ import annotations
import ast
import pytest
from typing import Any

def verifiable_python_ast_reward(completion: str, expected_signatures: list[str]) -> float:
    """Awards 1.0 for syntactically valid code containing required AST function defs."""
    try:
        tree = ast.parse(completion)
        func_names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
        for sig in expected_signatures:
            if sig not in func_names:
                return 0.1
        return 1.0
    except SyntaxError:
        return 0.0
```

---

## 2. Production Serving with vLLM & FP8 Quantization

### 2.1 PagedAttention & Prefix Caching
- **PagedAttention**: Partitions KV-cache into virtual memory blocks, eliminating memory fragmentation and reducing KV-cache waste from ~70% to <4%.
- **Automatic Prefix Caching (`--enable-prefix-caching`)**: Keeps static system prompt and `AGENTS.md` instructions cached in GPU VRAM across requests, dropping prompt TTFT (Time to First Token) by up to 85%.

### 2.2 FP8 (`torch.float8_e4m3fn`) Serving
- Quantizes model weights and activations to 8-bit floating point, cutting VRAM requirements in half compared to `bfloat16` while retaining >99.5% reasoning accuracy.
- Coupled with speculative decoding (draft models), vLLM achieves 2.5x–4x tokens/second per GPU.

---

## 3. Low-VRAM Optimization Profile (`@vram8`)
For video diffusion (DiT), super-resolution, and local inference within an 8 GB VRAM ceiling:
- **VAE Slicing & Tiling**: Processes image latents in spatial tiles to avoid OOM during decoding.
- **Sequential CPU Offload**: `pipeline.enable_sequential_cpu_offload()` streams layers from host RAM to GPU VRAM layer by layer.
- **Gradient Checkpointing**: `model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})`.
