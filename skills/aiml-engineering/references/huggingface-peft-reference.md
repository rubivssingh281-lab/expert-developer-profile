# Hugging Face Transformers & PEFT/LoRA Production Reference

Synthesized from **Hugging Face Official Documentation, PEFT Standards & vLLM Serving**.

---

## 1. Parameter-Efficient Fine-Tuning (LoRA & QLoRA)

### Mathematical Foundation of LoRA (Low-Rank Adaptation)
Rather than updating all $W_0 \in \mathbb{R}^{d \times k}$ parameters during fine-tuning, LoRA freezes $W_0$ and decomposes the weight update $\Delta W$ into two low-rank matrices:
$$W = W_0 + \Delta W = W_0 + \frac{\alpha}{r} (B \cdot A)$$
Where $A \in \mathbb{R}^{r \times k}$, $B \in \mathbb{R}^{d \times r}$, with rank $r \ll \min(d, k)$.
- Trainable parameters are reduced by $\ge 99\%$.
- $A$ is initialized with Gaussian distribution; $B$ is initialized to zero (so $\Delta W = 0$ at step 0).

### Production PEFT Configuration
```python
from peft import LoraConfig, get_peft_model, TaskType

lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,                         # Rank: 8 or 16 is optimal for most tasks
    lora_alpha=32,                # Alpha scaling factor (typically 2x rank)
    lora_dropout=0.05,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",   # Attention projections
        "gate_proj", "up_proj", "down_proj"       # MLP feed-forward layers
    ],
    bias="none",
)

model = get_peft_model(base_model, lora_config)
model.print_trainable_parameters()
```

---

## 2. 4-Bit Model Quantization (`BitsAndBytesConfig` / QLoRA)
To run large models on resource-constrained GPUs without accuracy degradation, configure 4-bit NormalFloat quantization:

```python
import torch
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,   # Computation dtype for linear operations
    bnb_4bit_quant_type="nf4",              # NormalFloat4: optimal for normally distributed weights
    bnb_4bit_use_double_quant=True,         # Nested quantization saves ~0.4 bits/param
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3-8B-Instruct",
    quantization_config=bnb_config,
    device_map="auto",
)
```

---

## 3. High-Throughput Inference Engines (vLLM)
For production LLM serving, avoid raw Hugging Face `generate()` loops due to naive KV cache allocation. Use **vLLM** with PagedAttention:
- **PagedAttention**: Manages Key-Value (KV) cache memory in virtual pages (analogous to virtual memory in operating systems), reducing KV memory waste from $60-80\%$ down to $< 4\%$.
- **Continuous Batching**: Dynamically inserts incoming requests into the current iteration instead of waiting for entire batch completion.

### vLLM Integration Pattern
```python
from vllm import LLM, SamplingParams

llm = LLM(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    tensor_parallel_size=1,      # Number of GPUs
    max_model_len=4096,
    gpu_memory_utilization=0.90,
)

sampling_params = SamplingParams(
    temperature=0.2,
    top_p=0.95,
    max_tokens=512,
)

prompts = ["Explain atomic state transitions in distributed databases:"]
outputs = llm.generate(prompts, sampling_params)
```

---

## 4. Tokenizer Invariants & Padding Rules
- **Padding Side**:
  - Training: Right-padding is standard.
  - Causal Generation (Inference): **Must use Left-Padding**! If right-padded, the model attempts to generate tokens continuing from the padding tokens, causing degraded or corrupted output.
- **EOS & PAD Tokens**:
  ```python
  if tokenizer.pad_token is None:
      tokenizer.pad_token = tokenizer.eos_token
  tokenizer.padding_side = "left"
  ```

---

## 5. Low-Latency Serving: Speculative Decoding & Chunked Prefill

### A. Speculative Decoding (Draft Models)
Memory bandwidth is the primary bottleneck during LLM autoregressive token decoding. Speculative decoding couples a smaller, faster **draft model** (e.g., Llama-3-1B) with the **target model** (e.g., Llama-3-70B):
1. The draft model generates $K$ candidate tokens speculatively in parallel.
2. The target model evaluates all $K$ tokens in a single forward pass.
3. Accepted tokens are emitted simultaneously, yielding $2\times - 3\times$ lower Inter-Token Latency (ITL) without altering the output distribution.

### B. Chunked Prefill Architecture
- **Problem**: When a long prompt arrives, standard schedulers run the full prefill eagerly, stalling ongoing token generation for all other concurrent requests and causing massive latency jitter.
- **Solution (`--enable-chunked-prefill`)**:
  - Slices incoming prompt sequences into smaller chunks (bounded by `--max-num-batched-tokens`, e.g., 512 or 2048 tokens).
  - Interleaves prefill chunks with decoding steps, ensuring active requests maintain consistent Time-To-Next-Token (TTNT) even under heavy prompt traffic.

