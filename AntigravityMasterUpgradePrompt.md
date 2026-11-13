# Master Upgrade Prompt for Antigravity (`expert-developer-profile`)

Copy the entire prompt below and paste it directly into **Antigravity** inside your [`expert-developer-profile`](https://github.com/rubivssingh281-lab/expert-developer-profile) workspace. It instructs the agent to perform an exhaustive, file-by-file expansion of your root instruction files, domain skills, reference manuals, golden production templates, verification harnesses, and episodic memory systems.

## Copyable Master Prompt

You are acting as a Principal Distinguished Software Architect, Staff Site Reliability Engineer, Principal Application Security Researcher, Staff Machine Learning Systems Engineer, and Lead Agentic Orchestration Architect. Your objective is to comprehensively upgrade and expand every file inside this repository ([`expert-developer-profile`](https://github.com/rubivssingh281-lab/expert-developer-profile)) so that it functions as an exhaustive, production-grade engineering knowledge base and parameterized instruction brain.

Do not summarize, abbreviate, or use placeholder comments (`// TODO`, `...`, `etc.`). Write out full architectural rules, exact configuration parameters, failure-mode tables, anti-pattern vs. best-practice code blocks, and concrete production blueprints across every file listed below.

### Phase 1: Upgrade Root Brain Files (`AGENTS.md` and `GEMINI.md`)

Expand both `AGENTS.md` and `GEMINI.md` so they enforce the following global engineering protocols across every task:

| Protocol Area | Mandatory Rules & Concrete Specifications to Write into `AGENTS.md` & `GEMINI.md` |
| :--- | :--- |
| **1. Parameterized Cognitive Control Plane** | Embed the formal 5-tuple state vector $\theta = \langle \tau, \sigma, \rho, \kappa, \delta \rangle$, mandatory execution header (`[COGNITIVE_STATE]` and `[ACTIVE_SKILLS]`), CLI `@mode` triggers (`@blitz`, `@fortress`, `@vram8`, `@vram24`, `@hyperscale`), and the 6-stage meta-cognitive control plane. |
| **2. Quantitative Capacity & ADR Engine** | Require quantitative capacity math (`[CAPACITY_MATH]`) for DB connection pool saturation, VRAM/KV-cache memory budgets, and SRE Little's Law / error budget burn rates. Enforce the Weighted Multi-Objective ADR utility function $U(A_k)$ for $\tau \ge 3$. |
| **3. Cross-Skill Orchestration Matrix** | Route tasks across all five specialized skills (`fastapi-backend-architecture`, `devops-engineering`, `cybersecurity-appsec`, `aiml-engineering`, and `agentic-orchestration`) with explicit handoffs and synthesis protocols. |
| **4. Pre-Implementation Architectural Audit** | Require a 5-point design verification before writing code: (a) Concurrency & event-loop safety; (b) Data integrity & transaction boundaries; (c) Trust boundary & threat modeling; (d) Backpressure, timeouts, and circuit breaking; (e) Observability (RED/USE, structured JSON logs via `structlog`, OpenTelemetry trace propagation). |
| **5. Strict Code & Typing Standards** | Enforce Python 3.11+ full type annotations (`from __future__ import annotations`, `Annotated`, `TypedDict`, `Protocol`, generics), strict Pydantic v2 validation (`ConfigDict(extra="forbid", strict=True)`), custom domain exception hierarchies mapped to RFC 9457 Problem Details (`application/problem+json`), and zero magic constants. |
| **6. Verification & Testing Gates** | Require unit, property-based, and async integration test patterns (`pytest`, `pytest-asyncio`, `httpx.AsyncClient` with lifespan overrides), deterministic database test fixtures, and static analysis compliance (`ruff`, `mypy --strict`, `bandit`). |

### Phase 2: Deepen `skills/fastapi-backend-architecture/`

Expand `skills/fastapi-backend-architecture/SKILL.md` and rewrite each file in `skills/fastapi-backend-architecture/references/` with deep, exhaustive production rules and code patterns:

1. **`references/fastapi-advanced-patterns.md`** (grounded in the [FastAPI Official Tutorial](https://fastapi.tiangolo.com/tutorial/) and [FastAPI Advanced User Guide](https://fastapi.tiangolo.com/advanced/)):
   - **ASGI & Event Loop Internals**: Explain the exact boundary between `async def` (runs directly on the single-threaded event loop; must never call blocking disk/network/CPU functions) and `def` endpoints (runs in AnyIO's worker threadpool), and when to use `asyncio.to_thread()` or `ProcessPoolExecutor`.
   - **Lifespan State Management**: Provide complete `@asynccontextmanager async def lifespan(app: FastAPI)` blueprints initializing database pools, Redis clients, HTTPX `AsyncClient` connection pools (with explicit connect/read/write/pool timeouts), and ML models on `app.state`.
   - **Dependency Injection Architecture**: Document multi-layered `Depends()` and `Security()` graphs, generator dependencies with `yield` and `try/finally` cleanup, request-scoped caching (`use_cache=True`), and test overrides via `app.dependency_overrides`.
   - **Resilience & High-Throughput Patterns**: Document idempotency-key middleware (backed by Redis/PostgreSQL locks), cursor-based keyset pagination (vs. `OFFSET` degradation), streaming responses, background task pitfalls (when to use FastAPI `BackgroundTasks` vs. durable queues like Celery/Arq/Temporal), and RFC 9457 exception handlers.

2. **`references/fowler-poeaa-complete-catalog.md`** (grounded in [Martin Fowler's Catalog of Patterns of Enterprise Application Architecture](https://martinfowler.com/eaaCatalog/)):
   - **Domain Logic Patterns**: Provide concrete Python implementations comparing **Transaction Script**, **Domain Model** (rich entities, value objects, and aggregates), and **Service Layer** orchestration.
   - **Data Source & Object-Relational Patterns**: Provide complete code blueprints for **Data Mapper** (decoupling domain entities from SQLAlchemy ORM models), **Repository Pattern** (abstracting persistence behind Python `Protocol` interfaces), **Unit of Work** (managing atomic commit/rollback boundaries across multiple repositories), **Identity Map**, and **Lazy Load** pitfalls in async Python (`MissingGreenlet` prevention via explicit `selectinload` / `joinedload`).
   - **Distributed & Concurrency Patterns**: Document **Optimistic Offline Lock** (version columns to prevent lost updates), **Pessimistic Offline Lock** (`SELECT ... FOR UPDATE SKIP LOCKED`), the **Transactional Outbox Pattern** (guaranteeing atomic database writes and event publishing), and **Saga orchestration** for multi-service workflows.

3. **`references/postgresql-18-internals.md`** (grounded in the [PostgreSQL 18 Official Documentation Manual](https://www.postgresql.org/docs/current/index.html)):
   - **MVCC, Vacuum & Tuple Visibility**: Explain Multi-Version Concurrency Control (`xmin`, `xmax`), dead tuple bloat, transaction ID wraparound protection, and per-table `autovacuum` tuning (`autovacuum_vacuum_scale_factor`, `autovacuum_vacuum_cost_limit`) for high-write tables.
   - **Advanced Indexing Playbook**: Provide decision matrices and DDL examples for **B-Tree** (composite column ordering, covering indexes with `INCLUDE`, partial indexes with `WHERE`), **GIN** (JSONB `jsonb_path_ops` and full-text search), **GiST**, **BRIN** (append-only time-series tables), and `pgvector` **HNSW** indexes for embeddings.
   - **Query Plan Optimization**: Document how to read `EXPLAIN (ANALYZE, BUFFERS, WAL, VERBOSE)`, resolve sequential scans, tune `work_mem`, `shared_buffers`, `effective_cache_size`, and `random_page_cost`, and rewrite slow `OFFSET` pagination into indexed keyset seeks (`WHERE (created_at, id) < ($1, $2)`).
   - **Connection Pooling & High Availability**: Document PgBouncer transaction-pooling rules (handling prepared statements in `asyncpg`, sizing pool limits using `(core_count * 2) + effective_spindle_count`), declarative partitioning (`PARTITION BY RANGE` / `HASH`), and Row-Level Security (RLS) for multi-tenant isolation.

### Phase 3: Deepen `skills/devops-engineering/`

Expand `skills/devops-engineering/SKILL.md` and rewrite each file in `skills/devops-engineering/references/` with complete production manifests and operational runbooks:

1. **`references/docker-buildkit-production.md`** (grounded in [Docker Building Best Practices](https://docs.docker.com/build/building/best-practices/)):
   - **Multi-Stage BuildKit Architecture**: Write complete production `Dockerfile` templates for Python/FastAPI and PyTorch workloads using `# syntax=docker/dockerfile:1`, `--mount=type=cache` for `uv`/`pip`/`apt`, and `--mount=type=secret` so build-time credentials never persist in image layers.
   - **Container Hardening & Minimal Base Images**: Document distroless and minimal slim images, non-root UID/GID execution (`USER 10001:10001`), read-only root filesystems, deterministic dependency locking, `.dockerignore` hygiene, `tini`/`dumb-init` PID 1 signal forwarding (`SIGTERM` graceful drain), and supply-chain verification (Cosign image signing, SBOM generation, and Trivy/Grype scanning).

2. **`references/kubernetes-mastery.md`** (grounded in the [Kubernetes Concepts Overview](https://kubernetes.io/docs/concepts/overview/), [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/), and [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)):
   - **Production Workload Manifests**: Provide complete YAML blueprints for `Deployment`, `StatefulSet`, `Service`, and Gateway API / Ingress with explicit `resources.requests` and `resources.limits` (explaining `Guaranteed` vs. `Burstable` QoS classes and avoiding CPU throttling traps).
   - **Zero-Downtime Rollouts & Probe Tuning**: Document `startupProbe` (protecting slow-loading ML models from premature restarts), `readinessProbe` (removing pods from service endpoints during overload), `livenessProbe`, `preStop` lifecycle sleep hooks (preventing 502 errors during Ingress endpoint propagation), `PodDisruptionBudget` (`minAvailable` / `maxUnavailable`), and `topologySpreadConstraints` across availability zones.
   - **Zero-Trust Security & Autoscaling**: Provide complete `SecurityContext` hardening (`runAsNonRoot: true`, `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`, `capabilities.drop: ["ALL"]`, `seccompProfile: RuntimeDefault`), default-deny + least-privilege Kubernetes NetworkPolicy manifests, and Horizontal Pod Autoscaler (`autoscaling/v2`) / KEDA configurations scaling on custom RPS or queue-depth metrics.

3. **`references/terraform-enterprise.md`** (grounded in the [HashiCorp Terraform Documentation](https://developer.hashicorp.com/terraform/docs)):
   - **Modular IaC Architecture**: Document multi-environment repository layouts (`modules/`, `environments/prod`, `environments/staging`), remote state backends with encryption and state locking, and strict provider/module version pinning.
   - **Defensive HCL Patterns**: Provide complete examples using `for_each` over `count` (preventing index-shift resource destruction), `variable` validation blocks, `precondition` and `postcondition` lifecycle checks, `moved` blocks for zero-downtime refactoring, `ephemeral` values / `sensitive = true` secret handling, and automated CI/CD plan/apply gates with `tflint`, `checkov`, and Open Policy Agent (OPA).

4. **`references/google-sre-handbook.md`** (grounded in the [Google Site Reliability Engineering (SRE) Book](https://sre.google/sre-book/table-of-contents/)):
   - **SLIs, SLOs, and Multi-Burn-Rate Alerting**: Provide exact Prometheus PromQL formulas for availability and latency percentile SLIs, error budget calculations, and multi-window multi-burn-rate alert rules (e.g., 2% budget burn in 1 hour and 5% in 6 hours) to eliminate alert fatigue.
   - **Overload Protection & Incident Engineering**: Document client-side adaptive throttling, load shedding, graceful degradation, jittered exponential backoff to prevent thundering herds, toil-elimination automation criteria, and blameless postmortem templates with action-item tracking.

### Phase 4: Deepen `skills/cybersecurity-appsec/`

Expand `skills/cybersecurity-appsec/SKILL.md` and rewrite each file in `skills/cybersecurity-appsec/references/` with concrete defensive code patterns and verification checklists:

1. **`references/owasp-cheat-sheets-guide.md`** (grounded in the [OWASP Top 10](https://owasp.org/projects/top-ten), [OWASP API Security Top 10](https://owasp.org/projects/api-security-project), and [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/IndexTopTen.html)):
   - **Authentication & Token Hardening**: Provide complete Python implementations for FastAPI OAuth2 JWT and OAuth2 Scopes using asymmetric `RS256`/`EdDSA` signing, explicit `iss`/`aud`/`exp`/`nbf`/`jti` claim validation, refresh token rotation with reuse detection, and Argon2id password hashing (`pwdlib`) with tuned memory, iteration, and parallelism parameters.
   - **API1–API10 Code-Level Mitigations**: Write out exact FastAPI/PostgreSQL code patterns preventing Broken Object Level Authorization (BOLA) (mandatory tenant/owner predicates in every SQL query and PostgreSQL RLS), Broken Object Property Level Authorization (strict separate read/write/update Pydantic DTOs), Unrestricted Resource Consumption (token-bucket rate limiting, payload size caps, pagination ceilings, query timeouts), and security headers (`Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options`, `Permissions-Policy`).

2. **`references/portswigger-attack-playbook.md`** (grounded in [PortSwigger Web Security Academy Topics](https://portswigger.net/web-security/all-topics)):
   - **Exploit Mechanics & Remediation Playbooks**: For each advanced vulnerability class—**SSRF** (Server-Side Request Forgery), **Insecure Deserialization**, **Race Conditions** (limit-overrun / TOCTOU), **OAuth2 Authorization Code / PKCE flaws**, **JWT algorithm confusion (`alg: none` / RS256-to-HS256)**, **GraphQL batching/introspection abuse**, **HTTP Request Smuggling**, **Web Cache Poisoning**, and **Web LLM Attacks** (indirect prompt injection, insecure output handling, sensitive data disclosure)—document:
     1. How the attack payload works against a vulnerable backend.
     2. The exact defensive code pattern in Python/FastAPI that neutralizes it (e.g., custom socket DNS resolution blocking RFC 1918 / link-local `169.254.169.254` cloud metadata IPs for SSRF; database row locking and atomic SQL increments for race conditions).

3. **`references/nist-csf-2-implementation.md`** (grounded in the [NIST Cybersecurity Framework (CSF) 2.0](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20)):
   - **Engineering Controls for All 6 Functions**: Map **Govern (GV)**, **Identify (ID)**, **Protect (PR)**, **Detect (DE)**, **Respond (RS)**, and **Recover (RC)** directly to automated technical controls in CI/CD and Kubernetes: SAST/DAST/SCA pipeline gates, secret scanning, Envelope Encryption (KMS + DEK rotation), immutable structured security audit logs, SIEM anomaly detection rules, automated credential revocation playbooks, and disaster-recovery backup restoration drills (RPO/RTO verification).

### Phase 5: Deepen `skills/aiml-engineering/`

Expand `skills/aiml-engineering/SKILL.md` and rewrite each file in `skills/aiml-engineering/references/` with production ML systems code and mathematical formulations:

1. **`references/pytorch-recipes-deep-dive.md`** (grounded in the [PyTorch Official Recipes Index](https://docs.pytorch.org/tutorials/recipes_index.html), [PyTorch Save and Load Guide](https://docs.pytorch.org/tutorials/beginner/basics/saveloadrun_tutorial.html), and [PyTorch Data Loading Optimization](https://docs.pytorch.org/tutorials/intermediate/intermediate_data_loading_tutorial.html)):
   - **High-Throughput Training & Profiling**: Provide complete code blueprints for `torch.amp.autocast` (`bfloat16`/`float16`) with `GradScaler`, `torch.compile(model, mode="max-autotune")`, gradient accumulation, gradient clipping (`clip_grad_norm_`), `DataLoader` tuning (`num_workers`, `pin_memory=True`, `persistent_workers=True`, `prefetch_factor`), and DistributedDataParallel (DDP) / Fully Sharded Data Parallel 2 (FSDP2).
   - **Safe & Low-Latency Production Inference**: Provide complete inference wrappers enforcing `torch.load(..., weights_only=True)` or `safetensors`, `model.eval()`, `torch.inference_mode()`, CUDA warmup passes, dynamic request batching with bounded wait queues (`max_batch_size`, `max_latency_ms`), TorchScript / ONNX export, and `torch.profiler` memory/latency bottleneck diagnosis.

2. **`references/huggingface-peft-reference.md`** (grounded in the [Hugging Face Transformers Quickstart](https://huggingface.co/docs/transformers/quicktour)):
   - **Parameter-Efficient Fine-Tuning (PEFT / LoRA / QLoRA)**: Explain the low-rank decomposition math ($\Delta W = B A \cdot \frac{\alpha}{r}$), hyperparameter selection rules for `r`, `lora_alpha`, `lora_dropout`, and `target_modules` (`q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`), 4-bit NormalFloat (`nf4`) quantization with `bitsandbytes` double quantization, and FlashAttention-2 integration.
   - **Production LLM Serving & RAG Architecture**: Document KV-cache memory math, vLLM PagedAttention block allocation, continuous batching, structured output generation, and production Retrieval-Augmented Generation (RAG) pipelines (semantic chunking, hybrid BM25 + dense vector retrieval, Reciprocal Rank Fusion, cross-encoder reranking, and grounded citation verification).

3. **`references/sklearn-google-ml-foundations.md`** (grounded in the [Scikit-Learn Official User Guide](https://scikit-learn.org/stable/user_guide.html) and [Google Machine Learning Foundational Courses](https://developers.google.com/machine-learning/foundational-courses)):
   - **Zero-Leakage Classical ML Pipelines**: Provide complete `Pipeline` and `ColumnTransformer` blueprints with custom `BaseEstimator` / `TransformerMixin` classes, nested cross-validation (`StratifiedKFold`, `TimeSeriesSplit` to prevent temporal lookahead leakage), probability calibration (`CalibratedClassifierCV`), and threshold tuning for asymmetric business costs (Precision-Recall AUC vs. ROC-AUC).
   - **Industrial ML Engineering Lifecycle**: Codify Google's rules of ML engineering—baseline heuristics before deep learning, training-serving skew prevention via unified feature transformations, data drift (Population Stability Index / KS test) and concept drift monitoring, shadow deployments, and canary rollouts.

### Phase 6: Create a `templates/` Directory with Golden Production Blueprints

Create a new `templates/` directory at the root of the repository and populate it with complete, copy-ready reference implementations that embody every rule in `skills/`:

1. `templates/fastapi-pytorch-service/main.py` — Complete async FastAPI + PyTorch + `asyncpg` + OAuth2 JWT scoped microservice with bounded `asyncio.Queue` dynamic micro-batching, lifespan management, BOLA protection, and structured logging.
2. `templates/docker/Dockerfile.production` — Hardened multi-stage BuildKit `Dockerfile` with cache mounts, non-root execution (`USER 10001:10001`), and minimal runtime surface.
3. `templates/kubernetes/production-stack.yaml` — Complete Kubernetes `Deployment`, `Service`, `HorizontalPodAutoscaler`, `PodDisruptionBudget`, and default-deny + allowlist `NetworkPolicy` manifests.
4. `templates/checklists/PR_ARCHITECTURE_SECURITY_CHECKLIST.md` — A rigorous pre-merge Staff Engineer code review checklist covering async safety, SQL performance, OWASP API security, container hardening, and ML serving reliability.

### Phase 7: Reflexion, Adversarial Self-Correction & Deterministic Verification Loops

Integrate executable verification loops into the agent's pre-commit and evaluation protocol:

1. **Automated Verification Harness (`templates/hooks/verify_blueprint.sh`)**:
   - Provide a deterministic bash script that executes static checks across the repository:
     - Python syntax and formatting: `ruff check` and `mypy --strict`.
     - Security static analysis: `bandit -r` with high-severity thresholds and regex-based secret scanning.
     - Container security: Enforcing `USER` non-root UID declaration, read-only root filesystems, and pinned base image digests.
     - Kubernetes manifest verification: Verifying resource requests and limits, securityContext settings, and probe configurations.
2. **Deterministic Reflexion Protocol**:
   - When any static check, test, or linter produces a failure, the agent must not blindly retry with guess-and-check edits.
   - Enforce an explicit 3-step Reflexion block:
     1. `[FAILURE_ROOT_CAUSE]`: Precise parsing of compiler/linter error output.
     2. `[INVARIANT_VIOLATION]`: Identify which architectural or language invariant was violated.
     3. `[DETERMINISTIC_REMEDIATION]`: Apply the minimal, exact surgical fix that preserves architectural invariants without regressing neighboring code.

### Phase 8: Episodic Project Memory & Cross-Skill Composition Graph

Establish persistent state tracking across sessions and chain all five domain skills into an acyclic execution graph:

1. **Episodic Memory Schema (`.agent/memory/`)**:
   - Maintain machine-readable state in `.agent/memory/project_state.schema.json` capturing:
     - Settled architectural decisions (ADRs) with their winning utility scores.
     - Hardware and runtime constraints (available GPU VRAM, target RPS, cloud provider).
     - Known bug root causes and regression test suites.
   - Provide `.agent/memory/adr_ledger_template.md` for recording structured architectural decision records.
2. **Cross-Skill Composition Graph**:
   - Formally connect all five skills into a deterministic Directed Acyclic Graph (DAG):
     - `agentic-orchestration` decomposes high-level goals into subtasks and manages tool schemas.
     - `fastapi-backend-architecture` ingests requests and orchestrates Unit of Work transactions.
     - `cybersecurity-appsec` filters payloads, validates tokens, and guards against OWASP/PortSwigger threats.
     - `aiml-engineering` serves model predictions via dynamic micro-batching and quantized pipelines.
     - `devops-engineering` wraps workloads into hardened BuildKit containers and resilient Kubernetes pods.
