# Staff Engineer Pull Request Architecture & Security Checklist

A mandatory pre-merge gate for all production code, services, and infrastructure changes.

---

## 1. Concurrency, Async Safety & Event Loop Hygiene
- [ ] **Zero Blocking I/O**: Are all file, network, and database operations strictly asynchronous inside `async def` routes?
- [ ] **Offloaded CPU & Legacy Calls**: Are heavy cryptographic hashing, image compression, or synchronous libraries wrapped in `await asyncio.to_thread()` or dispatched to worker queues?
- [ ] **Race Condition Prevention**: Are concurrent resource mutations (wallet deductions, counter increments, stock changes) protected via `SELECT ... FOR UPDATE`, atomic SQL CAS updates, or distributed Redis locks?
- [ ] **Timeout Enforcements**: Does every outgoing HTTP/gRPC request declare an explicit connect, read, and write timeout?

---

## 2. Data Integrity, SQL Performance & PostgreSQL 18
- [ ] **N+1 Elimination**: Are foreign key relations eagerly loaded using `selectinload` or `joinedload` rather than causing per-row lazy queries in loops?
- [ ] **Transaction Boundaries**: Are multi-entity mutations encapsulated within a single Unit of Work / scoped `AsyncSession` transaction?
- [ ] **Primary Key Design**: Do new stateful tables utilize `uuidv7()` to ensure sequential B-Tree index clustering and prevent index page bloat?
- [ ] **Query Plan Verification**: Has `EXPLAIN (ANALYZE, BUFFERS)` been verified on query changes to confirm that sequential scans on large tables are eliminated?
- [ ] **Connection Pooling**: Is database session acquisition bound to request lifespan dependencies, ensuring connections are committed/rolled back and returned immediately to the pool?

---

## 3. OWASP API Security & Threat Modeling
- [ ] **BOLA / IDOR Verification**: Does every database read, update, and delete query include an explicit `tenant_id == current_user.tenant_id` or `user_id == current_user.id` predicate?
- [ ] **Input Contract Strictness**: Are request payloads strictly typed with Pydantic v2 schemas using `model_config = ConfigDict(extra="forbid", strict=True)`?
- [ ] **Authentication & Scopes**: Are sensitive endpoints protected by asymmetric JWT verification (`RS256`/`EdDSA`) with explicit scope requirements (`Security(get_current_user, scopes=[...])`)?
- [ ] **Password & Secret Security**: Are passwords hashed using Argon2id ($m \ge 64\text{MB}, t \ge 3, p \ge 4$)? Are API keys compared using `hmac.compare_digest`?
- [ ] **SSRF Defense**: Are all user-supplied URLs pre-resolved and verified to block RFC 1918 private subnets and cloud metadata endpoints (`169.254.169.254`)?
- [ ] **Error Sanitization**: Are error payloads compliant with RFC 9457 Problem Details without exposing internal stack traces, system paths, or raw database messages?

---

## 4. Container Hardening & DevOps Reliability
- [ ] **Non-Root Execution**: Does the `Dockerfile` enforce unprivileged non-root user execution (`USER 10001:10001`)?
- [ ] **Minimal Runtime Surface**: Is the production image using multi-stage BuildKit builds with minimal distroless or slim bases, discarding compilers and dev-tools?
- [ ] **Read-Only Root Filesystem**: Does the container run with `readOnlyRootFilesystem: true`, mounting only transient scratch paths as `tmpfs`?
- [ ] **Probe Alignment**: Are `startupProbe`, `livenessProbe`, and `readinessProbe` configured with appropriate timeouts and period thresholds?
- [ ] **PreStop Hook**: Does the pod lifecycle include a `preStop: exec: command: ["/bin/sh", "-c", "sleep 5"]` hook to prevent 502 Bad Gateways during Ingress endpoint draining?

---

## 5. Machine Learning & Inference Safety
- [ ] **Inference Mode**: Is model evaluation strictly wrapped in `torch.inference_mode()` rather than legacy `torch.no_grad()`?
- [ ] **Device Placement & Warmup**: Is model weights loading executed during application `lifespan` startup with a dummy forward pass before opening network traffic?
- [ ] **Bounded Memory & Batching**: Are inference requests bounded by max sequence length caps and dynamic batching wait limits to eliminate GPU Out-Of-Memory (OOM) crashes?
- [ ] **Model Checkpoint Integrity**: Are models loaded strictly with `weights_only=True` or `safetensors` to prevent arbitrary code execution vulnerabilities during deserialization?
