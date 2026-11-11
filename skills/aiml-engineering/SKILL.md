---
name: aiml-engineering
description: >-
  Use this skill when building AI/ML applications, designing Retrieval-Augmented Generation (RAG) systems, training or fine-tuning models (PyTorch recipes, Hugging Face transformers, LoRA/PEFT), engineering classical ML pipelines (Scikit-Learn), deploying inference, or applying Google Machine Learning foundational principles.
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

## 3. PyTorch Canonical Recipes Standard

### High-Efficiency Training Loop with AMP (Automatic Mixed Precision)
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

---

## 4. Hugging Face Transformers & PEFT/LoRA Standards

### Inference & Tokenizer Hygiene
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)
# Ensure padding token is set
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    attn_implementation="flash_attention_2" if torch.cuda.is_available() else "eager",
)

# Explicit tokenization parameters
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

### Parameter-Efficient Fine-Tuning (PEFT / LoRA)
- Apply LoRA to attention projection weights (`q_proj`, `k_proj`, `v_proj`, `o_proj`).
- Set low rank `r=8` or `16`, `lora_alpha=16` or `32`, `lora_dropout=0.05` to adapt models with `< 1%` trainable parameters while preventing catastrophic forgetting.

---

## 5. Production RAG Architecture
- **Chunking**: Prefer semantic or recursive character splitting (500–1000 tokens) with 10–15% overlap.
- **Hybrid Retrieval**: Combine dense semantic search (vector embeddings via cosine similarity) and sparse keyword retrieval (BM25) with Reciprocal Rank Fusion (RRF).
- **Cross-Encoder Re-Ranking**: Rerank the top 25 candidates using a cross-encoder model to pass the 3–5 most relevant chunks to the generation prompt.
- **Structured Validation**: Require LLM outputs to adhere to Pydantic schemas using structured outputs / Instructor to guarantee valid API consumption.
