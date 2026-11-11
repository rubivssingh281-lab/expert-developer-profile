# 🚀 Expert Developer Profile for Antigravity & AI Agents

A production-grade, authoritative configuration package that transforms your AI coding agent into a **Principal Software Engineer & Technical Architect**.

This profile synthesizes standards, runbooks, and implementation recipes from **16 industry gold-standard references**:
1. **Kubernetes Concepts & Architecture** — `https://kubernetes.io/docs/concepts/overview/`
2. **Docker Building Best Practices (BuildKit)** — `https://docs.docker.com/build/building/best-practices/`
3. **Google Site Reliability Engineering (SRE) Book** — `https://sre.google/sre-book/table-of-contents/`
4. **HashiCorp Terraform Documentation** — `https://developer.hashicorp.com/terraform/docs`
5. **OWASP Top 10 Web Application Security Risks** — `https://owasp.org/projects/top-ten`
6. **OWASP Cheat Sheet Series (Top 10 Index)** — `https://cheatsheetseries.owasp.org/IndexTopTen.html`
7. **NIST Cybersecurity Framework (CSF) 2.0** — `https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20`
8. **PortSwigger Web Security Academy Topics** — `https://portswigger.net/web-security/all-topics`
9. **PyTorch Official Recipes Index** — `https://docs.pytorch.org/tutorials/recipes_index.html`
10. **Hugging Face Transformers Quickstart** — `https://huggingface.co/docs/transformers/quicktour`
11. **Scikit-Learn Official User Guide** — `https://scikit-learn.org/stable/user_guide.html`
12. **Google Machine Learning Foundational Courses** — `https://developers.google.com/machine-learning/foundational-courses`
13. **FastAPI Official Tutorial & User Guide** — `https://fastapi.tiangolo.com/tutorial/`
14. **FastAPI Advanced User Guide** — `https://fastapi.tiangolo.com/advanced/`
15. **PostgreSQL 18 Official Documentation Manual** — `https://www.postgresql.org/docs/current/index.html`
16. **Martin Fowler's Catalog of Enterprise Application Architecture (PoEAA)** — `https://martinfowler.com/eaaCatalog/`

---

## 📂 Package Architecture & Layout

```text
expert-developer-profile/
├── README.md                      # Complete reference documentation & index
├── install.sh                     # Automated 1-command installer script
├── GEMINI.md                      # Always-on Principal Architect Rules
├── AGENTS.md                      # Mirror rules file (for AGENTS.md standard)
└── skills/                        # On-demand specialized skills & deep-dive manuals
    ├── devops-engineering/
    │   ├── SKILL.md
    │   └── references/
    │       ├── docker-buildkit-production.md    # Multi-stage, cache mounts, secret mounts, rootless
    │       ├── kubernetes-mastery.md            # Workload controllers, 3-probe pattern, QoS, NetworkPolicies
    │       ├── google-sre-handbook.md           # SLI/SLO math, LIFO queue shedding, deadline propagation
    │       └── terraform-enterprise.md          # State locking, precondition/postcondition, moved blocks
    ├── cybersecurity-appsec/
    │   ├── SKILL.md
    │   └── references/
    │       ├── nist-csf-2-implementation.md     # 6 Core Functions (GV, ID, PR, DE, RS, RC), Tiers 1-4
    │       ├── owasp-cheat-sheets-guide.md      # OWASP 2025 Top 10, Argon2id, session rotation, mTLS
    │       └── portswigger-attack-playbook.md   # CL.TE/TE.CL smuggling, race conditions, JWT flaws, CORS
    ├── aiml-engineering/
    │   ├── SKILL.md
    │   └── references/
    │       ├── pytorch-recipes-deep-dive.md     # torchrun, DDP, DistributedSampler, AMP GradScaler
    │       ├── huggingface-peft-reference.md    # BitsAndBytesConfig (NF4/double quant), LoRA, vLLM
    │       └── sklearn-google-ml-foundations.md # Feature crosses, bucketing, ColumnTransformer pipeline
    └── fastapi-backend-architecture/
        ├── SKILL.md
        └── references/
            ├── fowler-poeaa-complete-catalog.md # Unit of Work, Repository, Optimistic/Pessimistic Locking
            ├── fastapi-advanced-patterns.md     # GzipRoute, SecurityScopes, yield deps, SSE streaming
            └── postgresql-18-internals.md       # Native AIO io_uring, Skip Scan, uuidv7(), failover=true
```

---

## 📚 Detailed Reference Manuals Summary

### 1. DevOps & Cloud Infrastructure
* **[docker-buildkit-production.md](./skills/devops-engineering/references/docker-buildkit-production.md)**: High-performance BuildKit caching (`--mount=type=cache`), build-time secret injection (`--mount=type=secret`), layer ordering rules, and rootless non-root runtime environments.
* **[kubernetes-mastery.md](./skills/devops-engineering/references/kubernetes-mastery.md)**: Production Workloads (Deployments, StatefulSets, DaemonSets), three-probe architecture (`startupProbe`, `livenessProbe`, `readinessProbe`), Guaranteed QoS matching, `preStop` sleep mechanics, and default-deny `NetworkPolicy`.
* **[google-sre-handbook.md](./skills/devops-engineering/references/google-sre-handbook.md)**: Mathematical SLI/SLO formulas, error budget burn rates ($14.4\times$ critical threshold), toil elimination (<50%), cascading failure defenses (**LIFO queue scheduling**, deadline propagation), and blameless post-mortems.
* **[terraform-enterprise.md](./skills/devops-engineering/references/terraform-enterprise.md)**: Encrypted remote state with DynamoDB locking, `precondition` and `postcondition` assertions, and zero-downtime state restructuring using `moved` blocks.

### 2. Cybersecurity & Application Security (AppSec)
* **[nist-csf-2-implementation.md](./skills/cybersecurity-appsec/references/nist-csf-2-implementation.md)**: Structure across the 6 core functions: **Govern (`GV`)**, **Identify (`ID`)**, **Protect (`PR`)**, **Detect (`DE`)**, **Respond (`RS`)**, **Recover (`RC`)**, including Organizational Profiles (Current vs. Target) and Implementation Tiers 1–4.
* **[owasp-cheat-sheets-guide.md](./skills/cybersecurity-appsec/references/owasp-cheat-sheets-guide.md)**: **OWASP Top 10:2025** alignment (A03 Supply Chain Failures, A10 Exceptional Conditions), Argon2id memory-hard hashing ($m \ge 64\text{MB}, t \ge 3, p \ge 4$), session rotation on privilege change, and microservices mTLS identity propagation.
* **[portswigger-attack-playbook.md](./skills/cybersecurity-appsec/references/portswigger-attack-playbook.md)**: Advanced exploits: HTTP Request Smuggling (CL.TE / TE.CL) defenses via end-to-end HTTP/2 and socket severing, concurrency race conditions (atomic CAS and `SELECT FOR UPDATE`), JWT algorithm confusion (`RS256` vs `HS256`), and CORS whitelist invariants.

### 3. AI / ML & LLM Systems Engineering
* **[pytorch-recipes-deep-dive.md](./skills/aiml-engineering/references/pytorch-recipes-deep-dive.md)**: Multi-GPU orchestration with `torchrun --nproc_per_node=N`, `dist.init_process_group(backend="nccl")`, epoch-aware `DistributedSampler`, Automatic Mixed Precision (`torch.amp.GradScaler`), and PyTorch Profiler.
* **[huggingface-peft-reference.md](./skills/aiml-engineering/references/huggingface-peft-reference.md)**: Parameter-Efficient Fine-Tuning (LoRA & QLoRA mathematical decomposition), 4-bit NormalFloat quantization (`BitsAndBytesConfig` with double quant and `bfloat16` compute), left-padding inference invariants, and vLLM PagedAttention serving.
* **[sklearn-google-ml-foundations.md](./skills/aiml-engineering/references/sklearn-google-ml-foundations.md)**: Elimination of data leakage (global preprocessing traps, temporal leakage, group leakage), Google ML feature engineering (**bucketing/binning** and **feature crosses**), PR-AUC evaluation, and composite `ColumnTransformer` + `Pipeline` standards.

### 4. FastAPI & Distributed Backend Architecture
* **[fowler-poeaa-complete-catalog.md](./skills/fastapi-backend-architecture/references/fowler-poeaa-complete-catalog.md)**: Martin Fowler's PoEAA catalog: Domain Model vs Transaction Script, Unit of Work (`AsyncSession`), Repository / Data Mapper separation, Service Layer, DTOs via Pydantic v2, and Optimistic (`version_id`) vs Pessimistic Offline Locking for long-running business transactions.
* **[fastapi-advanced-patterns.md](./skills/fastapi-backend-architecture/references/fastapi-advanced-patterns.md)**: Custom `APIRoute` subclassing (`GzipRequest`, `GzipRoute`, `TimedLoggingRoute`), fine-grained authorization via `OAuth2PasswordBearer` and `SecurityScopes`, yield dependencies with Redis connection pools, Server-Sent Events (SSE), and RFC 7807 Problem Details.
* **[postgresql-18-internals.md](./skills/fastapi-backend-architecture/references/postgresql-18-internals.md)**: PostgreSQL 18 Native Asynchronous I/O (`io_uring`), B-Tree **Skip Scan** index optimization, native `uuidv7()` timestamp-clustered primary keys, GIN `jsonb_path_ops`, BRIN indexing, MVCC mechanics, and logical replication failover (`failover = true` + `pg_createsubscriber`).

---

## ⚡ Installation Instructions

### Option A: Install Globally (Recommended)
Applies to **all projects and sessions** on your machine:

```bash
# Run the included installer
bash install.sh --global
```

Or manually:
```bash
mkdir -p ~/.gemini/config/skills
cp GEMINI.md ~/.gemini/config/
cp -r skills/* ~/.gemini/config/skills/
```

### Option B: Install in a Specific Repository / Project
Applies **only to that repository** and can be checked into git:

```bash
# In your target project root:
mkdir -p .agents/skills
cp /path/to/expert-developer-profile/AGENTS.md .agents/
cp -r /path/to/expert-developer-profile/skills/* .agents/skills/
```

---

## 📦 How to Share

1. **Copy the Folder**: Share `expert-developer-profile/` via USB, cloud drive, or SCP.
2. **Zip / Tar Archive**:
   ```bash
   tar -czvf expert-developer-profile.tar.gz expert-developer-profile/
   # or
   zip -r expert-developer-profile.zip expert-developer-profile/
   ```
3. **Publish to GitHub / GitLab**:
   ```bash
   cd expert-developer-profile
   git init
   git add .
   git commit -m "feat: complete expert developer profile synthesizing 16 standards"
   ```
