---
name: aiml-engineering
description: >-
  Use this skill when building AI/ML applications, designing Retrieval-Augmented Generation (RAG) systems, training or fine-tuning models (PyTorch recipes, Hugging Face transformers, LoRA/PEFT, FSDP2), engineering classical ML pipelines (Scikit-Learn), deploying inference, or applying Google Machine Learning foundational principles.
trigger_patterns:
  keywords: ["pytorch", "torch", "huggingface", "transformers", "peft", "lora", "qlora", "vllm", "sklearn", "model serving", "rag", "embeddings", "inference", "fsdp", "fsdp2", "amp", "gradscaler", "pagedattention"]
  file_globs: ["**/*model*.py", "**/*train*.py", "**/*infer*.py", "**/*rag*.py", "**/requirements*.txt", "**/pyproject.toml"]
  architectural_intents: ["model-training", "fine-tuning", "rag-pipeline", "inference-serving", "classical-ml-pipeline", "vram-capacity-optimization"]
theta_bindings:
  governing_parameters: ["kappa", "delta"]
  parameter_mappings:
    kappa:
      cpu-only: "Pure CPU inference, ONNX runtime, quantize to int8, avoid CUDA memory allocations"
      gpu-8gb-vram: "Enforce 4-bit NormalFloat (nf4) QLoRA, double quant, gradient checkpointing, peak VRAM <= 7.2GB ceiling"
      gpu-24gb-vram: "Single-GPU 16-bit inference or QLoRA batch size <= 16, FlashAttention-2, vLLM continuous batching"
      single-a100-80gb: "Full bfloat16 fine-tuning, large context window (32k+), vLLM PagedAttention with high KV-cache budget"
      multi-node-fsdp: "PyTorch FSDP2 per-parameter sharding using DTensor across multi-node cluster with epoch-aware DistributedSampler"
cross_skill_hooks:
  upstream:
    - skill: "fastapi-backend-architecture"
      contract: "Provides bounded asyncio.Queue and async request payload dispatch to dynamic micro-batch worker"
    - skill: "cybersecurity-appsec"
      contract: "Validates input sanitization, token bounds, and prompt injection defense before tensor encoding"
  downstream:
    - skill: "devops-engineering"
      contract: "Configures GPU resource requests/limits, CUDA runtime container, and KEDA autoscaling on queue depth"
lazy_references:
  - file: "references/pytorch-recipes-deep-dive.md"
    condition: "Activated when implementing PyTorch training, FSDP2, DDP, torch.compile, or low-latency inference loops"
  - file: "references/huggingface-peft-reference.md"
    condition: "Activated when designing LoRA/QLoRA fine-tuning, vLLM PagedAttention, KV-cache sizing, or RAG systems"
  - file: "references/sklearn-google-ml-foundations.md"
    condition: "Activated when building Scikit-Learn tabular pipelines, feature crosses, or evaluating data leakage"
---

# AI/ML, Deep Learning & LLM Systems Engineering Skill

Authoritative knowledge base, canonical code patterns, and production guidelines synthesizing standards from:
- **PyTorch Official Recipes Index** — [PyTorch Recipes & High-Performance Deep Learning Reference](./references/pytorch-recipes-deep-dive.md)
- **Hugging Face Transformers & PEFT** — [Hugging Face Transformers & PEFT/LoRA Production Reference](./references/huggingface-peft-reference.md)
- **Scikit-Learn & Google ML Foundations** — [Scikit-Learn & Google Machine Learning Foundations Reference](./references/sklearn-google-ml-foundations.md)

---

## 1. Google Machine Learning Foundational Principles

### A. Problem Framing & Data Hygiene
- **Data Leakage Elimination**:
  - Never fit transformers, scalers, or encoders on the complete dataset. Always fit on the training split *only*, then transform validation/test splits.
  - In time-series or sequential data, use temporal splits (`TimeSeriesSplit`), never random shuffle splits.
- **Class Imbalance Strategies**:
  - For skewed distributions, evaluate using Precision-Recall AUC (PR-AUC), F1-score, or Matthews Correlation Coefficient (MCC) rather than raw Accuracy.
  - Apply class weights, focal loss, or balanced sampling rather than naive random oversampling.
- **Regularization & Generalization**:
  - Guard against overfitting using early stopping with patience, dropout, and weight decay (L2 regularization).
  - Track train loss vs. validation loss; a diverging validation loss marks the onset of memorization.

---

## 2. Scikit-Learn Production Pipeline Standard

### Leak-Free Pipeline with ColumnTransformer & Cross-Validation
```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score

numeric_features = ["age", "income", "transaction_count"]
categorical_features = ["region", "subscription_tier"]

# Independent preprocessing streams
numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)

# Full composite model pipeline
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", HistGradientBoostingClassifier(random_state=42)),
])

# Cross-validation on stratified folds
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="roc_auc")
```

---

## 3. PyTorch Canonical Recipes & Distributed Training (FSDP2)

### A. High-Efficiency Training Loop with AMP (Automatic Mixed Precision)
```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MyNeuralNet().to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-2)
criterion = nn.CrossEntropyLoss()

# Automated Mixed Precision (AMP) Scaler for CUDA
scaler = torch.amp.GradScaler("cuda", enabled=(device.type == "cuda"))

train_loader = DataLoader(
    dataset,
    batch_size=64,
    shuffle=True,
    num_workers=4,
    pin_memory=(device.type == "cuda"),
    persistent_workers=True,
)

model.train()
for epoch in range(num_epochs):
    for batch_idx, (inputs, targets) in enumerate(train_loader):
        inputs = inputs.to(device, non_blocking=True)
        targets = targets.to(device, non_blocking=True)
        
        optimizer.zero_grad(set_to_none=True)  # Lower memory overhead than zero_grad()

        with torch.amp.autocast("cuda", enabled=(device.type == "cuda")):
            outputs = model(inputs)
            loss = criterion(outputs, targets)

        scaler.scale(loss).backward()
        
        # Gradient clipping to prevent exploding gradients
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        scaler.step(optimizer)
        scaler.update()

# Safe State-Dict Checkpointing
torch.save({
    "epoch": epoch,
    "model_state_dict": model.state_dict(),
    "optimizer_state_dict": optimizer.state_dict(),
    "scaler_state_dict": scaler.state_dict(),
}, "checkpoint.pt")
```

### B. PyTorch FSDP2 Memory Calculation Formula
When $\kappa = \text{multi-node-fsdp}$, calculate memory footprint per GPU rank ($M_{\text{FSDP2}}$):

$$M_{\text{FSDP2}} = \frac{\Psi \cdot B_{\text{param}}}{N} + \frac{\Psi \cdot B_{\text{grad}}}{N} + \frac{\Psi \cdot B_{\text{opt}}}{N} + M_{\text{unsharded\_layer}} + M_{\text{activations}}$$

Where $\Psi$ is total parameters, $N$ is rank count, $B_{\text{opt}} = 12$ bytes for AdamW (FP32 master weights + momentum + variance), and $M_{\text{unsharded\_layer}}$ is the peak transient memory of the currently executing transformer block brought in via `all-gather`.

---

## 4. Hugging Face Transformers & PEFT/LoRA Standards

### A. Inference & Tokenizer Hygiene
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    attn_implementation="flash_attention_2" if torch.cuda.is_available() else "eager",
)

inputs = tokenizer(
    "Synthesize the core invariants of distributed consensus:",
    return_tensors="pt",
    truncation=True,
    max_length=2048,
).to(model.device)

with torch.inference_mode():  # Faster and lower memory than torch.no_grad()
    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.2,
        top_p=0.9,
        repetition_penalty=1.1,
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id,
    )

response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
```

### B. vLLM PagedAttention KV-Cache Memory Formula
During production inference serving, calculate KV-cache memory per token across all layers:

$$\text{KV}_{\text{bytes/token}} = 2 \times L \times H_{\text{kv}} \times D_{\text{head}} \times B_{\text{dtype}}$$

The maximum concurrent token capacity is bounded by:

$$\text{Max Tokens} = \frac{(\text{VRAM}_{\text{total}} \times \text{gpu\_memory\_utilization}) - \text{VRAM}_{\text{weights}} - \text{VRAM}_{\text{overhead}}}{\text{KV}_{\text{bytes/token}}}$$

---

## 5. Production RAG Architecture
- **Chunking**: Prefer semantic or recursive character splitting (500–1000 tokens) with 10–15% overlap.
- **Hybrid Retrieval**: Combine dense semantic search (vector embeddings via cosine similarity) and sparse keyword retrieval (BM25) with Reciprocal Rank Fusion (RRF).
- **Cross-Encoder Re-Ranking**: Rerank the top 25 candidates using a cross-encoder model to pass the 3–5 most relevant chunks to the generation prompt.
- **Structured Validation**: Require LLM outputs to adhere to Pydantic schemas using structured outputs to guarantee valid API consumption.
