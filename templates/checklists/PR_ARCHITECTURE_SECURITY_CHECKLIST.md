# Staff Engineer Pull Request Architecture & Security Checklist (v2.0)

A mandatory pre-merge gate for all production code, services, agent workflows, and infrastructure changes across the 5 core engineering domains.

---

## 0. Cognitive State & Parameterized Envelope Verification
- [ ] **State Vector $\theta$ Explicitly Declared**: Does the implementation adhere to the instantiated $\theta = \langle \tau, \sigma, \rho, \kappa, \delta, \mu, \beta \rangle$?
- [ ] **Quantitative Capacity Math Proof (`[CAPACITY_MATH]`)**:
  - [ ] **Database Connection Pool**: Verified that `N_pods × N_workers × (pool + overflow) ≤ 0.80 × C_PgBouncerMax`?
  - [ ] **Compute Envelope (VRAM)**: If ML is involved, is total VRAM (weights + grads + optim + activations + KV-cache) bounded beneath `kappa_limit`?
  - [ ] **SRE Little's Law Concurrency**: Is concurrency capacity sized for `L = λ · W_P99` with bounded queue buffers?
- [ ] **Weighted ADR Evaluation (`[WEIGHTED_ADR]`)**: When $\tau \ge 3$, are candidate choices scored against the weighted utility function `U(A_k)`?

---

## 1. Concurrency, Async Safety & Event Loop Hygiene
- [ ] **Zero Blocking I/O**: Are all file, network, and database operations strictly asynchronous inside `async def` routes?
- [ ] **Offloaded CPU & Heavy Computations**: Are cryptographic operations, image transformations, and ML forward passes offloaded to `asyncio.to_thread` or worker queues?
- [ ] **Race Condition Prevention**: Are concurrent resource mutations protected via `SELECT ... FOR UPDATE`, atomic SQL CAS updates, or distributed Redis locks?
- [ ] **Bounded Queues & Dynamic Batching**: Are inference requests queued with `maxsize` limits and short collection timeouts (10–15ms) to prevent high P99 tail latency?

---

## 2. Data Integrity, SQL Performance & PostgreSQL 18
- [ ] **N+1 Query Elimination**: Are foreign key relations eagerly loaded using `selectinload` or `joinedload`?
- [ ] **Explicit Unit of Work Boundaries**: Are multi-entity mutations encapsulated within a single scoped `AsyncSession` transaction?
- [ ] **Sequential Indexing**: Do stateful tables utilize `uuidv7()` or sequential IDs to preserve B-Tree clustering and avoid page fragmentation?
- [ ] **Connection Lifecycle**: Are database sessions returned immediately to the pool via lifespan dependencies with `expire_on_commit=False`?

---

## 3. OWASP API Security & Threat Modeling
- [ ] **BOLA / IDOR Verification**: Does every database query include an explicit `tenant_id == current_user.tenant_id` or `user_id == current_user.id` predicate?
- [ ] **Defensive Schema Hygiene**: Are request payloads strictly typed with Pydantic v2 schemas using `model_config = ConfigDict(extra="forbid", strict=True)`?
- [ ] **Asymmetric Authentication**: Are protected endpoints verified with asymmetric JWT (`RS256`/`EdDSA`) and explicit permission scopes?
- [ ] **Password & Secret Security**: Are passwords hashed using Argon2id ($m \ge 64\text{MB}, t \ge 3, p \ge 4$)? Are API keys compared using `hmac.compare_digest`?
- [ ] **SSRF Defense**: Are all outbound HTTP requests filtered to block RFC 1918 private subnets and cloud metadata endpoints (`169.254.169.254`)?
- [ ] **RFC 9457 Error Masking**: Are error payloads sanitized into RFC 9457 Problem Details without leaking database errors, SQL queries, or internal stack traces?

---

## 4. Container Hardening & DevOps Reliability
- [ ] **Non-Root Execution**: Does the `Dockerfile` enforce unprivileged non-root user execution (`USER 10001:10001`)?
- [ ] **Minimal Runtime Surface**: Is the production image using multi-stage BuildKit builds with minimal distroless or slim bases?
- [ ] **Read-Only Root Filesystem**: Does the container run with `readOnlyRootFilesystem: true`, mounting only transient scratch paths as `tmpfs`?
- [ ] **Kubernetes Three-Probe Pattern**: Are `startupProbe`, `livenessProbe`, and `readinessProbe` configured with appropriate thresholds?
- [ ] **PreStop Hook**: Does the pod lifecycle include a `preStop` sleep hook to prevent 502 Bad Gateway errors during Ingress endpoint draining?

---

## 5. Machine Learning & Inference Safety
- [ ] **Inference Mode**: Is model evaluation wrapped in `@torch.inference_mode()` rather than legacy `torch.no_grad()`?
- [ ] **Device Placement & Warmup**: Is model weights loading executed during application `lifespan` startup with a pre-warm dummy forward pass?
- [ ] **CUDA OOM Recovery**: Does the inference loop handle `torch.cuda.OutOfMemoryError` gracefully by clearing caches and shedding load?
- [ ] **Model Checkpoint Integrity**: Are models loaded strictly with `weights_only=True` or `safetensors` to prevent arbitrary code execution vulnerabilities?

---

## 6. Agentic Orchestration & Prompt Guardrails
- [ ] **MCP Contract Strictness**: Are Model Context Protocol tools defined using JSON Schema Draft 2020-12 with `additionalProperties: false`?
- [ ] **Acyclic DAG Validation**: Has Kahn's algorithm or DFS 3-color cycle detection run prior to dispatching subagent execution graphs?
- [ ] **Dual-LLM Quarantine**: Are untrusted external inputs processed by quarantined models without tools before being parsed by privileged controllers?
- [ ] **Static Plan Locking**: Does the agent freeze its execution plan before executing tools to prevent indirect prompt injection hijacking?

---

## 7. Deterministic Verification Gate
- [ ] **Automated Script Execution**: Has `templates/hooks/verify_blueprint.sh` executed cleanly with 0 failures?
- [ ] **Zero Placeholders**: Verified zero instances of `TODO`, `FIXME`, or truncated code blocks in production files?
