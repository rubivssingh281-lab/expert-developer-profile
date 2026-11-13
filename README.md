# 🚀 Expert Developer Profile for Antigravity & AI Agents (v2.0 Parameterized Brain)

A production-grade, authoritative configuration package that transforms your AI coding agent into a **Principal Software Engineer, Technical Architect, and Lead Agentic Systems Engineer**.

Synthesizes standards, runbooks, and implementation recipes from **20+ industry gold-standard references**:
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
19. **Dual-LLM Security Pattern & Prompt Injection Mitigation**
20. **Multi-Agent DAG Topologies & Sliding-Window Token Economics**

---

## 📂 Package Architecture & Layout

```text
expert-developer-profile/
├── README.md                      # Complete reference documentation & index
├── install.sh                     # Parameterized multi-profile installer script
├── GEMINI.md                      # Always-on Principal Architect Rules (v2.0 Parameterized Brain)
├── AGENTS.md                      # Mirror rules file for multi-agent standard
├── AntigravityMasterUpgradePrompt.md # Master architectural upgrade prompt (Phases 1–8)
├── .agent/
│   └── memory/                    # Episodic long-term memory & ADR state tracking
│       ├── project_state.schema.json # JSON Schema (Draft 2020-12) for project state
│       └── adr_ledger_template.md    # Weighted ADR ledger template
├── templates/                     # Golden production blueprints & verification hooks
│   ├── fastapi-pytorch-service/
│   │   └── main.py                # 4-Skill Unified Contract: FastAPI + PyTorch + Dynamic Batching
│   ├── docker/
│   │   └── Dockerfile.production  # BuildKit multi-stage cache-mounted rootless container
│   ├── kubernetes/
│   │   └── production-stack.yaml  # Deployment, 3-probe, HPA, PDB, NetworkPolicy
│   ├── hooks/
│   │   └── verify_blueprint.sh    # Executable deterministic static analysis & container audit hook
│   └── checklists/
│       └── PR_ARCHITECTURE_SECURITY_CHECKLIST.md # Pre-merge Staff Engineer audit checklist
└── skills/                        # On-demand specialized skills with YAML frontmatter
    ├── devops-engineering/
    │   ├── SKILL.md
    │   └── references/            # Docker BuildKit, Kubernetes, Google SRE math, Terraform
    ├── cybersecurity-appsec/
    │   ├── SKILL.md
    │   └── references/            # NIST CSF 2.0, OWASP Top 10, PortSwigger attack vectors
    ├── aiml-engineering/
    │   ├── SKILL.md
    │   └── references/            # PyTorch FSDP2, PEFT/LoRA, vLLM PagedAttention, Scikit-Learn
    ├── fastapi-backend-architecture/
    │   ├── SKILL.md
    │   └── references/            # Fowler PoEAA, FastAPI advanced patterns, PostgreSQL 18 AIO
    └── agentic-orchestration/     # 5th Core Skill: Multi-agent execution & MCP contracts
        ├── SKILL.md
        └── references/
            ├── subagent-dag-decomposition.md    # Kahn's topological sort, fan-out/fan-in quorum
            ├── mcp-tool-schema-design.md        # MCP JSON-RPC 2.0, Draft 2020-12 inputSchema
            ├── context-compaction-memory.md     # Sliding window token budgeting, rolling compaction
            └── adversarial-prompt-guardrails.md # Dual-LLM quarantine, static plan locking
```

---

## 🧠 Parameterized Cognitive Control Plane ($\theta$-Vector)

Every architectural or implementation task is governed by the 5-tuple state vector:
$$\theta = \langle \tau, \sigma, \rho, \kappa, \delta \rangle$$

| Parameter | Allowed Domain Values | Operational Effect on Agent Brain |
| :--- | :--- | :--- |
| **Thinking Depth ($\tau$)** | `1` (Hotfix) \| `2` (Tactical) \| `3` (Architectural - Default) \| `4` (Formal-Proof) | Controls reasoning depth: $\tau=1$ bypasses ADR tables; $\tau=3$ enforces capacity math + weighted ADR; $\tau=4$ adds threat trees + property-based test suites. |
| **Scale Tier ($\sigma$)** | `local-edge` \| `startup-1k-rps` \| `growth-10k-rps` \| `hyperscale-100k-rps` | Shifts from single-node SQLite to PgBouncer, read-replicas, Redis Lua atomic rate limiting, and transactional outbox patterns. |
| **Security Posture ($\rho$)** | `prototype` \| `internal-prod` \| `zero-trust-public` (Default) \| `regulated-pci-hipaa` | Enforces mTLS, asymmetric JWT verification (`RS256`/`EdDSA`), BOLA/IDOR object-level ownership guards, and SSRF egress blocking. |
| **Compute Envelope ($\kappa$)** | `cpu-only` \| `gpu-8gb-vram` \| `gpu-24gb-vram` \| `single-a100-80gb` \| `multi-node-fsdp` | Selects 4-bit NormalFloat (`nf4`) QLoRA, double quant, and FlashAttention-2 when $\kappa \le \text{gpu-24gb-vram}$, or PyTorch FSDP2 when $\kappa = \text{multi-node-fsdp}$. |
| **Delivery Mode ($\delta$)** | `surgical-diff` \| `full-blueprint` (Default) \| `red-team-audit` | Controls output format: minimal unified diffs, zero-placeholder production modules, or exploit PoCs with remediation patches. |

### CLI Parameter Shorthand Macros (`@mode` Triggers)
- `@blitz` $\rightarrow \theta = \langle \tau=1, \sigma=\text{local-edge}, \rho=\text{internal-prod}, \kappa=\text{cpu-only}, \delta=\text{surgical-diff} \rangle$
- `@fortress` $\rightarrow \theta = \langle \tau=4, \sigma=\text{growth-10k-rps}, \rho=\text{zero-trust-public}, \kappa=\text{cpu-only}, \delta=\text{red-team-audit} \rangle$
- `@vram8` $\rightarrow \theta = \langle \tau=3, \sigma=\text{local-edge}, \rho=\text{internal-prod}, \kappa=\text{gpu-8gb-vram}, \delta=\text{full-blueprint} \rangle$
- `@vram24` $\rightarrow \theta = \langle \tau=3, \sigma=\text{startup-1k-rps}, \rho=\text{zero-trust-public}, \kappa=\text{gpu-24gb-vram}, \delta=\text{full-blueprint} \rangle$
- `@hyperscale` $\rightarrow \theta = \langle \tau=4, \sigma=\text{hyperscale-100k-rps}, \rho=\text{zero-trust-public}, \kappa=\text{multi-node-fsdp}, \delta=\text{full-blueprint} \rangle$

---

## ⚡ Installation Instructions

### Option A: Install Globally (Recommended)
Applies to **all projects and sessions** on your machine:

```bash
# Run the included installer
bash install.sh --global --profile default
```

### Option B: Install in a Specific Repository / Project
Applies **only to that repository** and initializes pre-commit verification hooks:

```bash
# In your target project root:
bash /path/to/expert-developer-profile/install.sh --project . --profile default --enable-pre-commit
```

---

## 🧪 Deterministic Verification Gate

Run the automated verification hook to validate all Python code, container specifications, and Kubernetes security contexts:

```bash
bash templates/hooks/verify_blueprint.sh
```
