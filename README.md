# 🚀 Expert Developer Profile for Antigravity & AI Agents (v3.0 Parameterized Brain)

A production-grade, authoritative configuration package that transforms your AI coding agent into a **Principal Software Engineer, Technical Architect, and Lead Agentic Systems Engineer**.

Synthesizes standards, runbooks, and implementation recipes from **25+ industry gold-standard references**:
1. **Kubernetes Concepts & Architecture** — `https://kubernetes.io/docs/concepts/overview/`
2. **Docker Building Best Practices (BuildKit)** — `https://docs.docker.com/build/building/best-practices/`
3. **Google Site Reliability Engineering (SRE) Book** — `https://sre.google/sre-book/table-of-contents/`
4. **HashiCorp Terraform Documentation** — `https://developer.hashicorp.com/terraform/docs`
5. **OWASP Top 10 Web Application Security Risks** — `https://owasp.org/projects/top-ten`
6. **OWASP API Security Top 10** — `https://owasp.org/projects/api-security-project`
7. **OWASP Cheat Sheet Series** — `https://cheatsheetseries.owasp.org/IndexTopTen.html`
8. **NIST Cybersecurity Framework (CSF) 2.0** — `https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20`
9. **PortSwigger Web Security Academy Topics** — `https://portswigger.net/web-security/all-topics`
10. **PyTorch Official Recipes & FSDP2** — `https://docs.pytorch.org/tutorials/recipes_index.html`
11. **Hugging Face Transformers & PEFT Quickstart** — `https://huggingface.co/docs/transformers/quicktour`
12. **Scikit-Learn Official User Guide** — `https://scikit-learn.org/stable/user_guide.html`
13. **Google Machine Learning Foundational Courses** — `https://developers.google.com/machine-learning/foundational-courses`
14. **FastAPI Official Tutorial & User Guide** — `https://fastapi.tiangolo.com/tutorial/`
15. **FastAPI Advanced User Guide** — `https://fastapi.tiangolo.com/advanced/`
16. **PostgreSQL 18 Official Documentation Manual** — `https://www.postgresql.org/docs/current/index.html`
17. **Martin Fowler's Catalog of Enterprise Application Architecture (PoEAA)** — `https://martinfowler.com/eaaCatalog/`
18. **Model Context Protocol (MCP) Specification** — `https://modelcontextprotocol.io/`
19. **Agent2Agent (A2A v1.0) Interoperability Standard**
20. **Contextual Agent Playbooks & Tools (CAPT) Architecture**
21. **eBPF Kernel Security (Cilium & Tetragon)**
22. **Reinforcement Learning with Verifiable Rewards (RLVR & GRPO)**
23. **Supply-Chain Provenance (SLSA Level 3 & Sigstore Cosign)**
24. **KEDA Event-Driven GPU & Queue Autoscaling**
25. **Context Engineering Runtime Patterns (arXiv:2507.13334)**

---

## 📂 Package Architecture & Layout

```text
expert-developer-profile/
├── .agent/
│   └── memory/                    # Episodic long-term memory & ADR state tracking
│       ├── project_state.schema.json # JSON Schema (Draft 2020-12) for project state
│       ├── adr_ledger_template.md    # Weighted ADR ledger template
│       ├── STATE.md               # Active agent harness state receipt
│       ├── PLAN.md                # Topological milestone DAG
│       └── IMPLEMENT.md           # Implementation audit ledger
├── .cursor/
│   └── rules/
│       └── expert-architect.mdc   # Cursor IDE alwaysApply configuration
├── .github/
│   ├── copilot-instructions.md    # GitHub Copilot Chat & Workspace directives
│   ├── PULL_REQUEST_TEMPLATE.md   # Staff-level PR audit template
│   └── workflows/
│       └── ci-verify.yml          # GitHub Actions verification pipeline
├── AGENTS.md                      # Universal agent cognitive rules
├── CLAUDE.md                      # Claude Code & Anthropic API bridge
├── GEMINI.md                      # Google Antigravity & Gemini CLI execution rules
├── AntigravityMasterUpgradePrompt.md # In-repo unabridged 10-phase upgrade prompt
├── README.md                      # Complete reference documentation & index
├── install.sh                     # Multi-profile & multi-harness installer script
├── scripts/
│   ├── validate_repo_integrity.py # Zero-dependency repo integrity, frontmatter & link linter
│   └── context_compactor.py       # Sliding-window context compaction utility
├── skills/                        # On-demand specialized skills with YAML frontmatter
│   ├── devops-engineering/
│   │   ├── SKILL.md
│   │   └── references/            # Docker BuildKit, Kubernetes, Google SRE math, Terraform, eBPF
│   ├── cybersecurity-appsec/
│   │   ├── SKILL.md
│   │   └── references/            # NIST CSF 2.0, OWASP Top 10, PortSwigger, SLSA Level 3
│   ├── aiml-engineering/
│   │   ├── SKILL.md
│   │   └── references/            # PyTorch FSDP2, PEFT/LoRA, Scikit-Learn, GRPO/FP8 vLLM, EDD/DeepEval
│   ├── data-engineering-observability/ # 7th Core Skill: Lean Lakehouse, Temporal & OTel
│   │   ├── SKILL.md
│   │   └── references/            # Apache Iceberg, Polars, DuckDB, Temporal durable execution, OTel
│   ├── fastapi-backend-architecture/
│   │   ├── SKILL.md
│   │   └── references/            # Fowler PoEAA, FastAPI advanced, PostgreSQL 18, pgvector RRF
│   ├── frontend-fullstack-engineering/ # 6th Core Skill: Modern Full-Stack Web & Playwright
│   │   ├── SKILL.md
│   │   └── references/            # React 19 Compiler, Next.js App Router/RSC, Server Actions, Playwright
│   └── agentic-orchestration/     # 5th Core Skill: Multi-agent execution & MCP contracts
│       ├── SKILL.md
│       └── references/            # MCP/A2A, CAPT playbooks, Spec-Driven Harnesses & Trajectory Evals
├── templates/                     # Golden production blueprints & verification hooks
│   ├── checklists/
│   │   └── PR_ARCHITECTURE_SECURITY_CHECKLIST.md
│   ├── docker/
│   │   └── Dockerfile.production  # BuildKit multi-stage cache-mounted rootless container
│   ├── fastapi-pytorch-service/
│   │   └── main.py                # FastAPI + PyTorch + Dynamic Batching + RFC 9457 errors
│   ├── hooks/
│   │   ├── verify_blueprint.sh    # Executable deterministic static analysis & test hook
│   │   └── maker_checker_loop.sh  # Maker/Checker parallel git worktree isolation harness
│   ├── kubernetes/
│   │   ├── production-stack.yaml  # Deployment, 3-probe, HPA, PDB, NetworkPolicy
│   │   └── keda-cilium-policy.yaml# Cilium L7 NetworkPolicy, Tetragon & KEDA ScaledObject
│   ├── mcp-server-fastapi/
│   │   └── server.py              # Production Streamable HTTP MCP & A2A v1.0 Server
│   └── playbooks/
│       └── incident_and_architecture_audit.j2.md # Parameterized Jinja2 incident runbook
└── tests/
    ├── test_integrity.py          # Pytest repo integrity and synchronization suite
    ├── test_fastapi_pytorch.py    # FastAPI + PyTorch integration tests
    └── test_mcp_server.py         # MCP JSON-RPC endpoints and A2A discovery tests
```

---

## 🧠 Parameterized Cognitive Control Plane ($\theta$-Vector)

Every architectural or implementation task is governed by the 7-tuple state vector:

```math
\theta = \langle \tau, \sigma, \rho, \kappa, \delta, \mu, \beta \rangle
```

| Parameter | Allowed Domain Values | Operational Effect on Agent Brain |
| :--- | :--- | :--- |
| **Thinking Depth ($\tau$)** | `1` (Hotfix), `2` (Tactical), `3` (Architectural), `4` (Formal-Proof) | Controls reasoning depth: $\tau=1$ bypasses ADR tables; $\tau=3$ enforces capacity math + weighted ADR; $\tau=4$ adds threat trees + property tests. |
| **Scale Tier ($\sigma$)** | `local-edge`, `startup-1k-rps`, `growth-10k-rps`, `hyperscale-100k-rps` | Shifts from single-node SQLite to PgBouncer, read-replicas, Redis Lua atomic rate limiting, and transactional outbox patterns. |
| **Security Posture ($\rho$)** | `prototype`, `internal-prod`, `zero-trust-public`, `regulated-pci-hipaa` | Enforces mTLS, asymmetric JWT verification (`RS256`/`EdDSA`), BOLA/IDOR object-level ownership guards, and SSRF egress blocking. |
| **Compute Envelope ($\kappa$)** | `cpu-only`, `gpu-8gb-vram`, `gpu-24gb-vram`, `single-a100-80gb`, `multi-node-fsdp2` | Selects 4-bit NormalFloat (`nf4`) QLoRA, double quant, and FlashAttention-2 when $\kappa \le \text{gpu-24gb-vram}$, or PyTorch FSDP2 when $\kappa = \text{multi-node-fsdp2}$. |
| **Delivery Mode ($\delta$)** | `surgical-diff`, `full-blueprint`, `adversarial-verifier`, `executable-playbook` | Controls output format: minimal unified diffs, zero-placeholder production modules, Maker/Checker audits, or Jinja2 CAPT playbooks. |
| **Memory Mode ($\mu$)** | `stateless`, `episodic-ledger`, `compacted-worktree` | Controls whether agent reads/writes `.agent/memory/STATE.md`, `PLAN.md`, and `adr_ledger_template.md`. |
| **Token Budget ($\beta$)** | `lean-5pct`, `standard-15pct`, `deep-research-35pct` | Controls lazy skill loading (<5% context window ceiling at startup). |

### CLI Parameter Shorthand Macros (`@mode` Triggers)
- `@blitz` $\rightarrow \langle \tau=1, \sigma=\text{local-edge}, \rho=\text{internal-prod}, \kappa=\text{cpu-only}, \delta=\text{surgical-diff}, \mu=\text{stateless}, \beta=\text{lean-5pct} \rangle$
- `@fortress` $\rightarrow \langle \tau=4, \sigma=\text{growth-10k-rps}, \rho=\text{regulated-pci-hipaa}, \kappa=\text{cpu-only}, \delta=\text{adversarial-verifier}, \mu=\text{episodic-ledger}, \beta=\text{deep-research-35pct} \rangle$
- `@checker` $\rightarrow \langle \tau=4, \sigma=\text{growth-10k-rps}, \rho=\text{zero-trust-public}, \kappa=\text{cpu-only}, \delta=\text{adversarial-verifier}, \mu=\text{episodic-ledger}, \beta=\text{standard-15pct} \rangle$
- `@vram8` $\rightarrow \langle \tau=3, \sigma=\text{local-edge}, \rho=\text{internal-prod}, \kappa=\text{gpu-8gb-vram}, \delta=\text{full-blueprint}, \mu=\text{episodic-ledger}, \beta=\text{lean-5pct} \rangle$
- `@vram24` $\rightarrow \langle \tau=3, \sigma=\text{startup-1k-rps}, \rho=\text{zero-trust-public}, \kappa=\text{gpu-24gb-vram}, \delta=\text{full-blueprint}, \mu=\text{episodic-ledger}, \beta=\text{standard-15pct} \rangle$
- `@hyperscale` $\rightarrow \langle \tau=4, \sigma=\text{hyperscale-100k-rps}, \rho=\text{zero-trust-public}, \kappa=\text{multi-node-fsdp2}, \delta=\text{full-blueprint}, \mu=\text{compacted-worktree}, \beta=\text{deep-research-35pct} \rangle$
- `@mcp-architect` $\rightarrow \langle \tau=3, \sigma=\text{growth-10k-rps}, \rho=\text{zero-trust-public}, \kappa=\text{cpu-only}, \delta=\text{full-blueprint}, \mu=\text{episodic-ledger}, \beta=\text{standard-15pct} \rangle$
- `@rag-hybrid` $\rightarrow \langle \tau=3, \sigma=\text{growth-10k-rps}, \rho=\text{zero-trust-public}, \kappa=\text{gpu-8gb-vram}, \delta=\text{full-blueprint}, \mu=\text{episodic-ledger}, \beta=\text{standard-15pct} \rangle$
- `@gitops-sre` $\rightarrow \langle \tau=3, \sigma=\text{growth-10k-rps}, \rho=\text{zero-trust-public}, \kappa=\text{cpu-only}, \delta=\text{full-blueprint}, \mu=\text{compacted-worktree}, \beta=\text{standard-15pct} \rangle$
- `@oss-maintainer` $\rightarrow \langle \tau=3, \sigma=\text{growth-10k-rps}, \rho=\text{zero-trust-public}, \kappa=\text{cpu-only}, \delta=\text{surgical-diff}, \mu=\text{stateless}, \beta=\text{lean-5pct} \rangle$

---

## ⚡ Installation Instructions

### Option A: Install Globally
Applies to **all projects and sessions** on your machine:

```bash
bash install.sh --global --profile default --harness all
```

### Option B: Install in a Specific Repository / Project
Applies **only to that repository** and initializes pre-commit verification hooks:

```bash
bash /path/to/expert-developer-profile/install.sh --project . --profile default --harness all --enable-pre-commit
```

---

## 🧪 Deterministic Verification Gate

Run the automated verification hook to validate all Python code, container specifications, and Kubernetes security contexts:

```bash
python3 scripts/validate_repo_integrity.py --check-math --check-sync
bash templates/hooks/verify_blueprint.sh
pytest tests/
```
