# Antigravity v3.0 Unabridged Master Upgrade Prompt: Autonomous Agent Harness, MCP/A2A Protocols, CAPT Playbooks, 10-Phase Pipeline & 2026 Production Engineering Stack

Copy the entire prompt below and paste it directly into **Google Antigravity** (or your autonomous coding agent CLI) at the root of [`rubivssingh281-lab/expert-developer-profile`](https://github.com/rubivssingh281-lab/expert-developer-profile).

***

## Master Execution Prompt (v3.0 Unabridged Production Edition)

You are operating as a **Distinguished Principal Systems Architect, Staff AI Harness Engineer, and Principal Security Researcher**. Your mission is to execute a complete, unabridged **v3.0 Architectural & Harness Upgrade** on this repository ([`rubivssingh281-lab/expert-developer-profile`](https://github.com/rubivssingh281-lab/expert-developer-profile)).

### Global Execution Rules for Antigravity & Autonomous Agents
1. **Zero Truncation & Zero Placeholders**: Never emit `// ... existing code ...`, `# TODO`, `pass`, or `[TBD]`. Write every file completely from line 1 to EOF.
2. **Fix Partial Commit State First**: Audit commit [`c34583b`](https://github.com/rubivssingh281-lab/expert-developer-profile/commit/c34583bdce9d84a978232ccdad142a5d299ff39b), where `skills/agentic-orchestration/` and the YAML frontmatter updates for existing skills were omitted from the working tree. Ensure every file in the directory tree below exists on disk and passes automated verification.
3. **Deterministic Self-Verification**: After writing all files across Phases 1–10, execute `python3 scripts/validate_repo_integrity.py --check-math --check-sync` and `bash templates/hooks/verify_blueprint.sh`, fixing any failure before declaring completion.
4. **Falsifiable Rules Over Directives**: Pair every architectural invariant with an automated static or runtime enforcement layer (`RULE-01` through `RULE-07`).
5. **Atomic Rollback & State Persistence**: Maintain `.agent/memory/STATE.md`, `PLAN.md`, and `IMPLEMENT.md` across every execution milestone to ensure clean context resumption and zero state drift.

***

## Target v3.0 Repository Tree

Ensure the repository populates and validates every file in this exact structure:

```text
expert-developer-profile/
├── .agent/
│   └── memory/
│       ├── project_state.schema.json         # Draft 2020-12 schema for agent state
│       ├── adr_ledger_template.md            # Weighted Multi-Objective ADR scoring ledger
│       ├── STATE.md                          # Active parameter vector, verified receipt & blockers
│       ├── PLAN.md                           # Milestone DAG with Kahn's topological sequencing
│       └── IMPLEMENT.md                      # Audit trail of modified files, diffs & receipts
├── .cursor/
│   └── rules/
│       └── expert-architect.mdc              # Cursor MDC configuration with alwaysApply rules
├── .github/
│   ├── copilot-instructions.md               # GitHub Copilot Chat & Workspace agent directives
│   ├── PULL_REQUEST_TEMPLATE.md              # Staff-level PR audit checklist & math bounds
│   └── workflows/
│       └── ci-verify.yml                     # Python 3.12 CI pipeline with AST/Lint/Type/Security gates
├── AGENTS.md                                 # Universal agent rules (7-Tuple θ, 10 macros, MathJax fixed)
├── CLAUDE.md                                 # Claude Code & Anthropic API bridge rules
├── GEMINI.md                                 # Google Antigravity & Gemini CLI execution rules
├── AntigravityMasterUpgradePrompt.md         # In-repo master architectural upgrade prompt
├── README.md                                 # Complete documentation, architecture index & tables
├── install.sh                                # Multi-profile installer with harness flags & verification
├── scripts/
│   ├── validate_repo_integrity.py            # Zero-dependency integrity, frontmatter, link & math linter
│   └── context_compactor.py                  # Token-efficient episodic context compaction utility
├── skills/
│   ├── agentic-orchestration/
│   │   ├── SKILL.md                          # 5th Core Skill: MCP, A2A, CAPT, Maker/Checker
│   │   └── references/
│   │       ├── mcp-a2a-protocol-architecture.md
│   │       ├── capt-executable-playbooks.md
│   │       └── context-compaction-and-worktrees.md
│   ├── aiml-engineering/
│   │   ├── SKILL.md                          # YAML frontmatter standardized
│   │   └── references/
│   │       ├── pytorch-recipes-deep-dive.md
│   │       ├── huggingface-peft-reference.md
│   │       ├── sklearn-google-ml-foundations.md
│   │       └── rlvr-grpo-vllm-fp8-serving.md  # 2026 Deep Dive: GRPO, PagedAttention, FP8, VAE tiling
│   ├── cybersecurity-appsec/
│   │   ├── SKILL.md                          # YAML frontmatter standardized
│   │   └── references/
│   │       ├── owasp-cheat-sheets-guide.md
│   │       ├── nist-csf-2-implementation.md
│   │       ├── portswigger-attack-playbook.md
│   │       └── agentic-llm-supply-chain-slsa3.md # 2026 Deep Dive: Dual-LLM, Prompt Injection, Cosign
│   ├── devops-engineering/
│   │   ├── SKILL.md                          # YAML frontmatter standardized
│   │   └── references/
│   │       ├── kubernetes-mastery.md
│   │       ├── docker-buildkit-production.md
│   │       ├── google-sre-handbook.md
│   │       ├── terraform-enterprise.md
│   │       └── ebpf-cilium-tetragon-keda-gitops.md # 2026 Deep Dive: Cilium L7, Tetragon, KEDA GPU
│   └── fastapi-backend-architecture/
│       ├── SKILL.md                          # YAML frontmatter standardized
│       └── references/
│           ├── fastapi-advanced-patterns.md
│           ├── postgresql-18-internals.md
│           ├── fowler-poeaa-complete-catalog.md
│           └── hybrid-pgvector-outbox-idempotency.md # 2026 Deep Dive: HNSW+BM25 RRF, Outbox, Idempotency
├── templates/
│   ├── checklists/
│   │   └── PR_ARCHITECTURE_SECURITY_CHECKLIST.md
│   ├── docker/
│   │   └── Dockerfile.production             # BuildKit multi-stage cache-mounted rootless container
│   ├── fastapi-pytorch-service/
│   │   └── main.py                           # FastAPI + PyTorch + Dynamic Batching + RFC 9457 errors
│   ├── hooks/
│   │   ├── verify_blueprint.sh               # Executable deterministic static analysis & test gate
│   │   └── maker_checker_loop.sh             # Git worktree isolation with Maker/Checker adversarial loop
│   ├── kubernetes/
│   │   ├── production-stack.yaml             # Deployment, 3-probe, HPA, PDB, NetworkPolicy
│   │   └── keda-cilium-policy.yaml           # Cilium L7 NetworkPolicy, Tetragon & KEDA ScaledObject
│   ├── mcp-server-fastapi/
│   │   └── server.py                         # Production Streamable HTTP MCP & A2A v1.0 Server
│   └── playbooks/
│       └── incident_and_architecture_audit.j2.md # CAPT Jinja2 parameterized incident playbook
└── tests/
    ├── test_integrity.py                     # Pytest suite for repo integrity, frontmatter & links
    ├── test_fastapi_pytorch.py               # Integration tests for FastAPI + PyTorch service
    └── test_mcp_server.py                    # Test suite for MCP JSON-RPC endpoints & A2A discovery
```

***

## Phase 1: Root Brain Directives (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`) & LaTeX Math Repair

Update [`AGENTS.md`](https://github.com/rubivssingh281-lab/expert-developer-profile/blob/main/AGENTS.md) and [`GEMINI.md`](https://github.com/rubivssingh281-lab/expert-developer-profile/blob/main/GEMINI.md), and create [`CLAUDE.md`](https://github.com/rubivssingh281-lab/expert-developer-profile/blob/main/CLAUDE.md) as a synchronized bridge following the [AGENTS.md Open Standard](https://agents.md/), [2026 CLAUDE.md & AgentLint Best Practices](https://www.agentlint.app/blog/claude-md-best-practices-2026), and [Context Engineering Runtime Patterns](https://www.artifilog.com/posts/context-engineering-for-ai-agents-runtime-systems).

### 1.1 Fix Broken GitHub MathJax Rendering in Section 6 (`[CAPACITY_MATH]`)
Unescaped underscores inside inline `$` expressions cause GitHub MathJax to throw `'_' allowed only in math mode` and fail rendering. Replace Section 6 with clean fenced ````math` blocks:

````markdown
## 6. Mandatory Quantitative Capacity Math Gates (`[CAPACITY_MATH]`)

Whenever `τ >= 3`, you MUST compute and emit concrete back-of-the-envelope capacity bounds before writing implementation code:

### 6.1 Database & Asynchronous Backend Gate
Verify connection pool limits, Little's Law concurrency, and memory overhead against [PostgreSQL 18 Internals](https://www.postgresql.org/docs/current/index.html) and [FastAPI Advanced Concurrency](https://fastapi.tiangolo.com/advanced/):

```math
\text{MaxConnections} = N_{\text{pods}} \times N_{\text{workers}} \times (\text{PoolSize} + \text{MaxOverflow}) \le 0.80 \times C_{\text{PgBouncerMax}}
```

```math
L_{\text{concurrency}} = \lambda_{\text{RPS}} \times W_{\text{P99LatencySec}}, \quad \text{RAM}_{\text{pod}} = \text{RAM}_{\text{base}} + N_{\text{workers}} \times \text{RAM}_{\text{worker}} \le 0.85 \times \text{K8sMemoryLimit}
```

### 6.2 AI/ML Training, Fine-Tuning & Inference VRAM Gate
Verify GPU memory footprint against hardware envelope $\kappa$ per [PyTorch Memory Recipes](https://docs.pytorch.org/tutorials/recipes_index.html) and [Hugging Face PEFT](https://huggingface.co/docs/transformers/quicktour):

```math
\text{VRAM}_{\text{train}} = \underbrace{P \cdot B_{\text{param}}}_{\text{Weights}} + \underbrace{P \cdot B_{\text{grad}}}_{\text{Gradients}} + \underbrace{P \cdot B_{\text{opt}}}_{\text{Optimizer States}} + \underbrace{B_{\text{batch}} \cdot S_{\text{seq}} \cdot H_{\text{dim}} \cdot L_{\text{layers}} \cdot \alpha_{\text{ckpt}}}_{\text{Activations}} \le 0.90 \times \kappa_{\text{VRAM}}
```

```math
\text{VRAM}_{\text{KV}} = 2 \times B_{\text{batch}} \times S_{\text{context}} \times L_{\text{layers}} \times N_{\text{kv\_heads}} \times d_{\text{head}} \times B_{\text{dtype}}
```

- **Automatic Hardware Fallback Rule**: If $\text{VRAM}_{\text{train}} > 0.90 \times \kappa_{\text{VRAM}}$, automatically enable 4-bit NormalFloat (`nf4`) QLoRA double quantization, gradient checkpointing (`use_reentrant=False`), paged 8-bit AdamW (`paged_adamw_8bit`), or CPU offloading without waiting for user prompting.
````

### 1.2 Expand the Execution Parameter Vector $\theta$ to a 7-Tuple Control Plane
Upgrade the cognitive parameter header in `AGENTS.md`, `GEMINI.md`, and `CLAUDE.md` to the **7-Tuple State Vector** $\theta = \langle \tau, \sigma, \rho, \kappa, \delta, \mu, \beta \rangle$:

| Parameter Symbol | Name | Allowed Values | Default Value | Behavioral Effect on Agent Execution |
| :--- | :--- | :--- | :--- | :--- |
| **$\tau$** | `thinking_depth` | `1` (Hotfix), `2` (Tactical), `3` (Architectural), `4` (Formal Proof) | `3` | Controls depth: $\tau=1$ bypasses ADR tables; $\tau=3$ enforces capacity math + weighted ADR; $\tau=4$ adds threat trees + property tests (`hypothesis`). |
| **$\sigma$** | `scale_tier` | `local-edge`, `startup-1k-rps`, `growth-10k-rps`, `hyperscale-100k-rps` | `growth-10k-rps` | Selects architecture from single-node SQLite to `asyncpg` + PgBouncer, read-replicas, Redis Lua limiters, and Transactional Outbox + Kafka. |
| **$\rho$** | `security_posture` | `prototype`, `internal-prod`, `zero-trust-public`, `regulated-pci-hipaa` | `zero-trust-public` | Dictates strictness of OWASP API Top 10, Dual-LLM prompt isolation, mTLS, Cosign image signing, and SLSA Level 3 provenance. |
| **$\kappa$** | `compute_envelope` | `cpu-only`, `gpu-8gb-vram`, `gpu-24gb-vram`, `single-a100-80gb`, `multi-node-fsdp2` | `gpu-8gb-vram` | Selects quantization (`nf4` vs `fp8` vs `bf16`), batch sizing, VAE/spatiotemporal tiling, and vLLM PagedAttention memory fraction. |
| **$\delta$** | `delivery_mode` | `surgical-diff`, `full-blueprint`, `adversarial-verifier`, `executable-playbook` | `full-blueprint` | Controls output format: minimal diff, complete zero-placeholder production module, Maker/Checker audit, or Jinja2 CAPT playbook. |
| **$\mu$** | `memory_mode` | `stateless`, `episodic-ledger`, `compacted-worktree` | `episodic-ledger` | Controls whether agent reads/writes `.agent/memory/STATE.md`, `PLAN.md`, and `adr_ledger_template.md` before/after tasks. |
| **$\beta$** | `token_budget` | `lean-5pct`, `standard-15pct`, `deep-research-35pct` | `lean-5pct` | Enforces lazy skill loading: loads only YAML frontmatter at startup (<5% window) and reads references on demand. |

### 1.3 Add 10 Fully Bound CLI `@mode` Shorthand Macros
Configure these 10 one-token macros with explicit 7-tuple bindings in `AGENTS.md`, `GEMINI.md`, and `CLAUDE.md`:

```text
1.  @blitz          -> θ = ⟨τ=1, σ=local-edge,       ρ=internal-prod,      κ=cpu-only,         δ=surgical-diff,        μ=stateless,          β=lean-5pct⟩
2.  @fortress       -> θ = ⟨τ=4, σ=growth-10k-rps,   ρ=regulated-pci-hipaa,κ=cpu-only,         δ=adversarial-verifier, μ=episodic-ledger,    β=deep-research-35pct⟩
3.  @checker        -> θ = ⟨τ=4, σ=growth-10k-rps,   ρ=zero-trust-public,  κ=cpu-only,         δ=adversarial-verifier, μ=episodic-ledger,    β=standard-15pct⟩
4.  @vram8          -> θ = ⟨τ=3, σ=local-edge,       ρ=internal-prod,      κ=gpu-8gb-vram,     δ=full-blueprint,       μ=episodic-ledger,    β=lean-5pct⟩
5.  @vram24         -> θ = ⟨τ=3, σ=startup-1k-rps,   ρ=zero-trust-public,  κ=gpu-24gb-vram,    δ=full-blueprint,       μ=episodic-ledger,    β=standard-15pct⟩
6.  @hyperscale     -> θ = ⟨τ=4, σ=hyperscale-100k,  ρ=zero-trust-public,  κ=multi-node-fsdp2, δ=full-blueprint,       μ=compacted-worktree, β=deep-research-35pct⟩
7.  @mcp-architect  -> θ = ⟨τ=3, σ=growth-10k-rps,   ρ=zero-trust-public,  κ=cpu-only,         δ=full-blueprint,       μ=episodic-ledger,    β=standard-15pct⟩
8.  @rag-hybrid     -> θ = ⟨τ=3, σ=growth-10k-rps,   ρ=zero-trust-public,  κ=gpu-8gb-vram,     δ=full-blueprint,       μ=episodic-ledger,    β=standard-15pct⟩
9.  @gitops-sre     -> θ = ⟨τ=3, σ=growth-10k-rps,   ρ=zero-trust-public,  κ=cpu-only,         δ=full-blueprint,       μ=compacted-worktree, β=standard-15pct⟩
10. @oss-maintainer -> θ = ⟨τ=3, σ=growth-10k-rps,   ρ=zero-trust-public,  κ=cpu-only,         δ=surgical-diff,        μ=stateless,          β=lean-5pct⟩
```

### 1.4 Add the Mandatory Falsifiable Rule Enforcement Table
Pair every rule with its concrete deterministic verification layer:

| Rule ID | Falsifiable Engineering Rule | Deterministic Enforcement Layer | Failure Action |
| :--- | :--- | :--- | :--- |
| **`RULE-01`** | Zero untyped functions or `Any` leaks in Python interfaces | `mypy --strict` in `verify_blueprint.sh` & CI | Block commit / Fail CI |
| **`RULE-02`** | Zero blocking sync I/O (`requests`, `time.sleep`, sync ORM) in `async def` | `ruff check --select ASYNC,B,S,E,F` | Block commit / Fail CI |
| **`RULE-03`** | Zero hardcoded secrets, weak hashes (`md5`/`sha1`), or unsafe `torch.load` | `bandit -r . -ll` + AST check in validator | Block commit / Fail CI |
| **`RULE-04`** | All error responses must conform to RFC 9457 (`application/problem+json`) | `pytest` contract assertions in service test suite | Fail test suite |
| **`RULE-05`** | Every query in multi-tenant routes must bind `tenant_id`/`owner_id` (BOLA) | SQLAlchemy scope guard / `@checker` review | Reject PR in Checker |
| **`RULE-06`** | Every `skills/*/SKILL.md` must have valid YAML & resolve all relative links | `python3 scripts/validate_repo_integrity.py` | Block commit / Fail CI |
| **`RULE-07`** | Root `AGENTS.md`, `GEMINI.md`, `CLAUDE.md` must be synchronized & math-clean | `python3 scripts/validate_repo_integrity.py --check-math --check-sync` | Block commit / Fail CI |

***

## Phase 2: Build the Missing 5th Skill (`skills/agentic-orchestration/`)

Create the complete `skills/agentic-orchestration/` directory that was missed in commit [`c34583b`](https://github.com/rubivssingh281-lab/expert-developer-profile/commit/c34583bdce9d84a978232ccdad142a5d299ff39b).

### 2.1 `skills/agentic-orchestration/SKILL.md`
Write `skills/agentic-orchestration/SKILL.md` with complete YAML frontmatter and production architecture rules:

```markdown
---
name: agentic-orchestration
version: "3.0.0"
description: "Enterprise multi-agent orchestration, Model Context Protocol (MCP) servers, Agent2Agent (A2A v1.0) interoperability, CAPT executable playbooks, Maker/Checker verification loops, and context compaction."
trigger_conditions:
  file_globs:
    - "**/mcp*/**/*.py"
    - "**/agents/**/*.py"
    - "**/playbooks/**/*.j2*"
    - ".agent/**/*"
    - "AGENTS.md"
    - "GEMINI.md"
    - "CLAUDE.md"
  intent_keywords:
    - "agent"
    - "subagent"
    - "MCP"
    - "Model Context Protocol"
    - "A2A"
    - "Agent2Agent"
    - "playbook"
    - "context engineering"
    - "compaction"
    - "worktree"
    - "prompt injection"
parameter_bindings:
  default_tau: 3
  min_security_posture: "zero-trust-public"
  default_memory_mode: "episodic-ledger"
cross_skill_hooks:
  - target_skill: "cybersecurity-appsec"
    condition: "external_tool_execution_or_untrusted_context_ingestion"
    required_checks: ["Dual-LLM quarantine", "MCP OAuth 2.1 scope validation", "SSRF allowlist"]
  - target_skill: "fastapi-backend-architecture"
    condition: "http_sse_or_streamable_http_mcp_transport"
    required_checks: ["anyio TaskGroup cancellation", "idempotency key locking", "OpenTelemetry GenAI spans"]
enforcement_commands:
  - "python3 scripts/validate_repo_integrity.py"
  - "bash templates/hooks/verify_blueprint.sh"
---

# Agentic AI & Multi-Agent Orchestration Skill (v3.0)

## 1. Core Architectural Primitives (The 2026 6-Primitive Agent Stack)
Every autonomous workflow you design MUST explicitly implement the six foundational primitives of Context & Harness Engineering:
1. **Filesystem-as-Interface**: Expose system state, schemas, logs, and runbooks as structured files on disk rather than proliferating brittle single-purpose tools.
2. **Externalized Durable Memory (`.agent/memory/`)**: Read `STATE.md` and `PLAN.md` at session start; update `STATE.md`, `IMPLEMENT.md`, and `adr_ledger_template.md` before session termination.
3. **Maker/Checker Adversarial Split**: Never allow the *Implementer* agent instance to self-certify production readiness. Route verification through an independent *Checker* persona (`@checker`) with a default `REJECT` stance.
4. **Git Worktree Parallel Isolation**: When spawning parallel sub-agents across independent modules, isolate each worker in a dedicated `git worktree add ../wt-<task-id> -b agent/<task-id>` directory to prevent working-tree race conditions.
5. **Protocol Interoperability (MCP + A2A v1.0)**:
   - Use the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for vertical **Agent-to-Tool** and **Agent-to-Resource** connections.
   - Use the [Agent2Agent (A2A v1.0) Protocol](https://aiworkaudit.net/guides/latest-ai-terminology-agentic-workflows-2026-trending-terms/) for horizontal **Agent-to-Agent** discovery (`/.well-known/agent.json`), task lifecycle negotiation, and cross-boundary artifact handoff.
6. **Skills & CAPT Playbooks as Intent-Debt Payment**: Encode repeatable multi-step institutional workflows as parameterized Jinja2 [Contextual Agent Playbooks & Tools (CAPT)](https://www.zenml.io/llmops-database/contextual-agent-playbooks-and-tools-enterprise-scale-ai-coding-agent-integration) exposed as typed MCP tools.

## 2. Token Budget & Context Compaction Rules
- **Startup Context Ceiling**: Pre-load only skill metadata (`name`, `description`, `trigger_conditions`) at session startup (<5% of context window).
- **Lazy Reference Loading**: Read files in `references/*.md` only when their domain matches `[ACTIVE_SKILLS]`.
- **Sliding-Window Summarization Gate**: When conversation trajectory exceeds 65% of the active context window, invoke `python3 scripts/context_compactor.py` to checkpoint verified facts, file paths, and open blockers into `.agent/memory/STATE.md` and prune raw intermediate tool logs.

## 3. Deep-Dive Reference Manuals
- `references/mcp-a2a-protocol-architecture.md` — Streamable HTTP MCP transports, OAuth 2.1 resource server scoping, JSON-RPC 2.0 error codes, and A2A v1.0 Agent Card / Task Lifecycle schemas.
- `references/capt-executable-playbooks.md` — Designing Jinja2-templated executable playbooks exposed via MCP tool definitions.
- `references/context-compaction-and-worktrees.md` — Context rot mitigation, deterministic compaction receipts, and parallel `git worktree` orchestration scripts.
```

### 2.2 Write the 3 Reference Manuals in `skills/agentic-orchestration/references/`
1. **`mcp-a2a-protocol-architecture.md`**:
   - Document complete MCP specification (Prompts, Resources, Tools, Sampling, Roots) using Streamable HTTP (`/mcp`) with SSE fallback, Pydantic v2 JSON Schema generation, tool annotation hints (`readOnlyHint`, `destructiveHint`, `idempotentHint`), and OAuth 2.1 + PKCE Bearer token validation.
   - Document A2A v1.0 protocol: schema for `/.well-known/agent.json` (`AgentCard`), JSON-RPC methods `tasks/send`, `tasks/sendSubscribe`, `tasks/get`, `tasks/cancel`, and state machine (`submitted -> working -> input-required -> completed | failed | canceled`).
   - Include complete Python adapter showing how an agent orchestrates remote subagents via MCP-to-A2A bridges.
2. **`capt-executable-playbooks.md`**:
   - Detail the LinkedIn Contextual Agent Playbooks & Tools (CAPT) Architecture: replacing brittle runbooks with Jinja2 playbooks (`templates/playbooks/*.j2.md`) exposed as typed MCP tools.
   - Include complete implementation of a `PlaybookRegistry` class validating input variables with Pydantic v2, rendering playbooks with `StrictUndefined`, and attaching deterministic verification commands.
3. **`context-compaction-and-worktrees.md`**:
   - Detail the 3-pillar context engineering taxonomy: Retrieval & Generation, Processing, and Management.
   - Provide the complete `git worktree` orchestration protocol for parallel subagents: branch isolation, collision-free database/port allocation, and Maker/Checker merge gates.

***

## Phase 3: Standardize YAML Frontmatter & Expand Domain Skills with 2026 High-Demand Tech

Standardize YAML frontmatter across `skills/cybersecurity-appsec/SKILL.md`, `skills/devops-engineering/SKILL.md`, and `skills/fastapi-backend-architecture/SKILL.md`, ensuring all 5 skills share the identical schema (`name`, `version`, `description`, `trigger_conditions`, `parameter_bindings`, `cross_skill_hooks`, `enforcement_commands`).

Next, create the 4 brand-new **2026 High-Demand Reference Manuals**:

### 3.1 `skills/aiml-engineering/references/rlvr-grpo-vllm-fp8-serving.md`
- **Reinforcement Learning with Verifiable Rewards (RLVR) & GRPO**:
  - Mathematical formulation of Group Relative Policy Optimization (GRPO), eliminating the critic network to save ~50% VRAM:
    ```math
    \mathcal{J}_{\text{GRPO}}(\theta) = \mathbb{E}_{q, \{o_i\}_{i=1}^G} \left[ \frac{1}{G} \sum_{i=1}^G \left( \min\left( r_i(\theta) \hat{A}_i, \text{clip}(r_i(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_i \right) - \beta \mathbb{D}_{\text{KL}}(\pi_\theta \| \pi_{\text{ref}}) \right) \right]
    ```
    where $\hat{A}_i = \frac{R(q, o_i) - \text{mean}(\{R(q, o_j)\})}{\text{std}(\{R(q, o_j)\}) + \varepsilon}$.
  - Complete Python training recipe using deterministic AST/pytest/math reward verifiers with 4-bit QLoRA (`nf4`) fitting inside an 8 GB–24 GB VRAM budget.
- **Production LLM Serving with vLLM & FP8 Quantization**:
  - Configuring PagedAttention, Automatic Prefix Caching (`--enable-prefix-caching`), Speculative Decoding (ngram/Medusa/Eagle), and Guided Decoding (FSM-enforced JSON schemas).
  - FP8 (`torch.float8_e4m3fn`) dynamic quantization and regional `torch.compile(model, mode="max-autotune")`.
- **Low-VRAM (`@vram8`) Video Diffusion & Super-Resolution Optimization**:
  - VAE slicing/tiling, sequential CPU offloading, gradient checkpointing (`use_reentrant=False`), chunked cross-entropy, and `torch.amp.autocast("cuda", dtype=torch.bfloat16)`.

### 3.2 `skills/fastapi-backend-architecture/references/hybrid-pgvector-outbox-idempotency.md`
- **PostgreSQL 18 Hybrid Retrieval (`pgvector` HNSW + BM25 + Reciprocal Rank Fusion)**:
  - Complete SQL and SQLAlchemy 2.0 `asyncpg` implementation combining dense vector similarity (`halfvec`/`vector` with relaxed order HNSW iterative scan) and full-text search fused via Reciprocal Rank Fusion:
    ```math
    \text{RRF\_Score}(d) = \frac{w_{\text{vec}}}{k + \text{rank}_{\text{vec}}(d)} + \frac{w_{\text{lex}}}{k + \text{rank}_{\text{lex}}(d)}, \quad k = 60
    ```
  - Mandatory tenant isolation predicate (`WHERE tenant_id = :tenant_id`) preventing cross-tenant vector leakage (OWASP API1:2023 BOLA).
- **Transactional Outbox Pattern & Idempotency-Key Middleware**:
  - ACID transaction inserting business entity and `outbox_events` row simultaneously, paired with an async `SKIP LOCKED` relay worker.
  - Complete ASGI Idempotency-Key Middleware using UUIDv7 keys, SHA-256 request payload fingerprinting (`422` on mismatch), and atomic lock leasing (`409` on in-flight duplicate).
- **Structured Concurrency & OpenTelemetry GenAI Semantic Conventions**:
  - Using `anyio.create_task_group()` with explicit cancellation scopes (`move_on_after`), plus OpenTelemetry GenAI spans recording token usage and P99 latency.

### 3.3 `skills/cybersecurity-appsec/references/agentic-llm-supply-chain-slsa3.md`
- **Agentic AI & MCP Threat Model (Indirect Prompt Injection & Confused Deputy Defense)**:
  - **Dual-LLM Quarantine Architecture**: Strict isolation between the Privileged Planner LLM (holds tools and schemas, never reads raw untrusted strings) and the Quarantined Reader LLM (zero tool access, extracts typed Pydantic models/enums from untrusted data).
  - **MCP Tool-Call Sandboxing & SSRF Protection**: Path traversal resolution check (`is_relative_to`), blocking private/metadata IP ranges (`127.0.0.0/8`, `169.254.169.254/32`), and requiring human confirmation tokens for mutating operations.
- **SLSA Level 3 Supply-Chain Provenance, Sigstore Cosign & CycloneDX SBOM**:
  - Hash-pinned dependency lockfiles, automated CycloneDX SBOM generation, `trivy` container scanning, and keyless container image signing via Sigstore Cosign with GitHub Actions OIDC.

### 3.4 `skills/devops-engineering/references/ebpf-cilium-tetragon-keda-gitops.md`
- **eBPF Cloud-Native Networking & Runtime Enforcement (Cilium + Tetragon)**:
  - Complete `CiliumNetworkPolicy` manifest enforcing L7 HTTP path/method rules and DNS egress allowlisting between FastAPI pods, PyTorch/vLLM workers, and PostgreSQL 18.
  - Complete Tetragon `TracingPolicy` CRD detecting and blocking (`Sigkill`) any unauthorized process execution (`/bin/sh`, `curl`, `wget`) inside distroless containers.
- **KEDA GPU & Queue Autoscaling + Multi-Window Multi-Burn-Rate SLOs**:
  - Complete `keda.sh/v1alpha1` `ScaledObject` manifest scaling GPU inference pods based on Prometheus `vllm:num_requests_waiting` and queue depth with stabilization windows.
  - Complete Google SRE Multi-Window Multi-Burn-Rate Prometheus Alerting Rules wired into ArgoCD automated rollback hooks.

***

## Phase 4: Create Externalized Durable Memory & Multi-Tool IDE Bridges

### 4.1 `.agent/memory/STATE.md`, `PLAN.md` & `IMPLEMENT.md`
Create `.agent/memory/STATE.md`, `PLAN.md`, and `IMPLEMENT.md` ensuring strict adherence to `.agent/memory/project_state.schema.json`:

```markdown
# Active Agent Harness State (`STATE.md`)

- **Schema Version**: `3.0.0`
- **Active Parameter Vector (`θ`)**:
  - `τ (thinking_depth)`: `3` (Architectural)
  - `σ (scale_tier)`: `growth-10k-rps`
  - `ρ (security_posture)`: `zero-trust-public`
  - `κ (compute_envelope)`: `gpu-8gb-vram`
  - `δ (delivery_mode)`: `full-blueprint`
  - `μ (memory_mode)`: `episodic-ledger`
  - `β (token_budget)`: `lean-5pct`
- **Last Verification Receipt**:
  - Command: `python3 scripts/validate_repo_integrity.py --check-math --check-sync && bash templates/hooks/verify_blueprint.sh`
  - Status: `PASS (Exit Code 0)`
- **Active Worktrees**: `main` (primary)
- **Open Blockers**: None
```

### 4.2 `.cursor/rules/expert-architect.mdc` & `.github/copilot-instructions.md`
1. **`.cursor/rules/expert-architect.mdc`**: Configure Cursor MDC frontmatter (`description`, `globs: ["**/*"]`, `alwaysApply: true`) instructing Cursor to bind `AGENTS.md`, read `.agent/memory/STATE.md`, and lazy-load active skills.
2. **`.github/copilot-instructions.md`**: Direct GitHub Copilot to instantiate the $\theta$-vector, enforce `RULE-01` through `RULE-07`, and execute `templates/hooks/verify_blueprint.sh`.

***

## Phase 5: Create Production MCP Server, CAPT Playbook & Maker/Checker Harness

### 5.1 `templates/mcp-server-fastapi/server.py`
Write a complete, runnable, strictly typed (`mypy --strict` clean) Python module implementing a production **Model Context Protocol (MCP)** & **CAPT Playbook** server using FastAPI + Pydantic v2:
- Implements JSON-RPC 2.0 endpoints (`tools/list`, `tools/call`, `resources/list`, `resources/read`) and an A2A v1.0 discovery route (`GET /.well-known/agent.json`) returning a validated `AgentCard`.
- Implements OAuth 2.1 Bearer token scope verification (`mcp:tools:read`, `mcp:tools:execute`), SSRF URL validation, path-traversal sandboxing, and RFC 9457 Problem Details error handling.
- Exposes a CAPT Playbook tool (`render_engineering_playbook`) that loads `templates/playbooks/incident_and_architecture_audit.j2.md`, validates inputs with Pydantic v2, and renders a deterministic remediation runbook.

### 5.2 `templates/playbooks/incident_and_architecture_audit.j2.md`
Create a Jinja2 executable playbook template accepting `service_name`, `scale_tier`, `security_posture`, `compute_envelope`, and `symptom_class`, rendering step-by-step diagnostic shell commands, SQL inspection queries, capacity math checks, and rollback criteria.

### 5.3 `templates/hooks/maker_checker_loop.sh`
Create an executable bash script (`chmod +x`) implementing the Maker/Checker Split & Git Worktree Isolation:
- Supports `--create-worktree <task_slug>`, `--verify-worktree <task_slug>`, and `--cleanup-worktree <task_slug>`.
- Runs `python3 scripts/validate_repo_integrity.py` and `bash templates/hooks/verify_blueprint.sh` inside the target worktree, writing a timestamped receipt to `.agent/memory/STATE.md`, and exiting non-zero (`REJECT`) on any failure.

### 5.4 `templates/kubernetes/keda-cilium-policy.yaml`
Provide the complete Kubernetes manifest bundle containing:
- `CiliumNetworkPolicy` (L7 HTTP ingress/egress filtering, DNS allowlisting, PostgreSQL/Kafka egress rules)
- Tetragon `TracingPolicy` (Process execution monitoring, Sigkill on unauthorized shells in container)
- KEDA `ScaledObject` (GPU inference auto-scaling based on Prometheus `vllm:num_requests_waiting` and queue depth with scale-down stabilization window)

***

## Phase 6: Write `scripts/validate_repo_integrity.py` & `scripts/context_compactor.py`

### 6.1 `scripts/validate_repo_integrity.py`
Write a complete, zero-dependency Python 3.11+ standard library validation script enforcing repository brain integrity:
1. **Skill Completeness Check**: Confirms all 5 skill directories exist and each contains `SKILL.md` plus a non-empty `references/` directory.
2. **YAML Frontmatter Schema Check**: Verifies that `name`, `version`, `description`, `trigger_conditions`, `parameter_bindings`, `cross_skill_hooks`, and `enforcement_commands` are present in all `skills/*/SKILL.md`.
3. **Relative Link Resolution Check**: Scans `README.md`, `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, and `skills/*/SKILL.md` for relative Markdown links and verifies that every referenced path exists on disk.
4. **GitHub LaTeX Math Linter (`--check-math`)**: Scans all `.md` files for inline `$...$` math blocks containing unescaped underscores outside `\text{...}` or unbalanced delimiters to prevent GitHub MathJax rendering errors.
5. **Root Brain Synchronization Check (`--check-sync`)**: Verifies that `AGENTS.md`, `GEMINI.md`, and `CLAUDE.md` contain matching section headers, `@mode` macros, and `RULE-01`..`RULE-07` enforcement IDs.

### 6.2 `scripts/context_compactor.py`
Write a zero-dependency Python 3.11+ CLI utility (`python3 scripts/context_compactor.py --state-file .agent/memory/STATE.md --adr-file .agent/memory/adr_ledger_template.md`) that reads `.agent/memory/STATE.md`, validates state invariants against `.agent/memory/project_state.schema.json`, and emits a compact `<SESSION_RESTORE_SNAPSHOT>` block (<400 tokens) ready to inject at the start of a new agent run.

***

## Phase 7: Upgrade `templates/hooks/verify_blueprint.sh` & CI Pipeline

### 7.1 `templates/hooks/verify_blueprint.sh`
Update `templates/hooks/verify_blueprint.sh` in strict mode (`set -euo pipefail`):
1. `python3 scripts/validate_repo_integrity.py --check-math --check-sync`
2. `python3 scripts/context_compactor.py --validate-only`
3. Python syntax & AST compilation across all `.py` files (`python3 -m py_compile scripts/*.py templates/fastapi-pytorch-service/main.py templates/mcp-server-fastapi/server.py`)
4. Static quality and security checks when available: `ruff check .`, `mypy --strict`, `bandit -r templates/ scripts/ -ll`, and `pytest`.

### 7.2 `.github/workflows/ci-verify.yml` & `.github/PULL_REQUEST_TEMPLATE.md`
- Create `.github/workflows/ci-verify.yml` for automated GitHub Actions verification on push/PR under Python 3.12.
- Create `.github/PULL_REQUEST_TEMPLATE.md` requiring contributors and agents to record the active **$\theta$-Vector**, **Capacity Math Bounds (`[CAPACITY_MATH]`)**, **Falsifiable Rules Checked (`RULE-01`..`RULE-07`)**, and **Checker Verification Output**.

***

## Phase 8: Upgrade `install.sh`, `README.md` & Golden Documentation

1. **Upgrade `install.sh`**:
   - Add support for `--profile <all|backend|aiml|devops|security|agentic>` and `--harness <all|antigravity|gemini|claude|cursor|copilot>` to install the v3.0 brain into any repository in a single command, running automated post-install validation.
2. **Upgrade `README.md`**:
   - Document the **v3.0 Autonomous Agent Harness & Parameterized Brain**, including the 7-tuple $\theta$-vector table, all 10 `@mode` macros, the 5 verified skills (linking all 19 deep-dive reference manuals), the Maker/Checker workflow, the MCP/A2A/CAPT templates, and the CI verification pipeline.
   - Ensure all math formulas in `README.md` use clean fenced ````math` blocks that render without error on GitHub.

***

## Phase 9: Comprehensive Golden Test Suite & Hypothesis Property Testing

Create an automated test suite under `tests/` validating all system layers:

### 9.1 `tests/test_integrity.py`
Pytest suite that executes `scripts/validate_repo_integrity.py` programmatically, verifying:
- All 5 skill directories and their 19 reference manuals exist.
- All YAML frontmatter blocks parse and validate against required fields.
- All internal Markdown relative links resolve to existing files.
- Zero LaTeX math errors or unescaped underscores exist across the codebase.

### 9.2 `tests/test_fastapi_pytorch.py`
Async integration test suite using `httpx.AsyncClient`:
- Verifies FastAPI lifespan startup, health probes (`/health/live`, `/health/ready`), and model inference routes.
- Asserts RFC 9457 Problem Details response structure on validation and internal errors (`application/problem+json`).
- Tests Idempotency-Key header deduplication and concurrent lock rejection.

### 9.3 `tests/test_mcp_server.py`
Automated test suite verifying the production MCP and A2A server:
- Asserts `GET /.well-known/agent.json` returns valid A2A v1.0 `AgentCard`.
- Tests JSON-RPC 2.0 `tools/list` and `tools/call` for `render_engineering_playbook`.
- Tests OAuth 2.1 Bearer scope rejection (`401 Unauthorized` / `403 Forbidden`) and SSRF private IP blocking.

### 9.4 `tests/test_hypothesis_properties.py`
Property-based testing with `hypothesis`:
- Fuzzes input schemas, UUIDv7 idempotency keys, and tenant authorization decorators to prove absence of injection vulnerabilities or BOLA leakage.

***

## Phase 10: Antigravity 2.0 Native Integration, Swarm Delegation & Final Verification

### 10.1 Antigravity Slash Command & Tool Alignment
Ensure seamless integration with Google Antigravity's native agent capabilities:
- **Slash Commands**: Recommend and document `/goal` (long-running autonomous tasks), `/plan` (hierarchical DAG planning), `/grill-me` (interactive ADR interview), `/teamwork` (subagent swarm orchestration), `/learn` (persisting learned rules), `/boost` (deep-thinking verification), `/compact` (rolling context compaction), and `/schedule` (cron and timer triggers).
- **Artifact Management**: Structure persistent plans, checklists, and reports within `<appDataDir>/brain/<conversation-id>` with `ArtifactMetadata`.
- **Subagent Swarms**: Utilize `invoke_subagent` and `manage_subagents` with dedicated roles (e.g., `Architect`, `Maker`, `Checker`, `AppSec Auditor`).

### 10.2 Final Deterministic Verification Execution
Run the complete end-to-end verification sequence:
```bash
python3 scripts/validate_repo_integrity.py --check-math --check-sync
python3 scripts/context_compactor.py --validate-only
bash templates/hooks/verify_blueprint.sh
pytest tests/
git status
```
Verify that every directory and file across all 10 phases exists, compiles cleanly, passes all static quality and security gates, and has zero unresolved placeholders.
