---
name: agentic-orchestration
description: >-
  Use this skill when designing multi-agent workflows, Directed Acyclic Graph (DAG) task decomposition, Model Context Protocol (MCP) tool schemas, rolling context compaction, episodic memory retention, or implementing adversarial prompt injection guardrails for autonomous agents.
trigger_patterns:
  keywords: ["agent", "multi-agent", "subagent", "mcp", "tool schema", "dag", "topological sort", "fan-out", "fan-in", "prompt injection", "context compaction", "dual-llm", "episodic memory"]
  file_globs: ["**/*agent*.py", "**/*tool*.py", "**/*mcp*.py", "**/*workflow*.py", "**/*orchestrat*.py", "**/.agent/**"]
  architectural_intents: ["multi-agent-coordination", "dag-pipeline-execution", "mcp-server-design", "context-compaction", "prompt-guardrail-hardening", "agentic-memory-sync"]
theta_bindings:
  governing_parameters: ["tau", "delta"]
  parameter_mappings:
    tau:
      1: "Single-agent direct execution, no subagent DAG decomposition"
      2: "Linear 2-stage worker-verifier handoff"
      3: "Full DAG decomposition with topological sort, cycle detection, and fan-out/fan-in quorum"
      4: "Formal proof verification DAG, dual-LLM quarantine isolation, and property-based test harness"
cross_skill_hooks:
  upstream: []
  downstream:
    - skill: "fastapi-backend-architecture"
      contract: "Dispatches structured MCP tool execution calls to backend endpoints"
    - skill: "cybersecurity-appsec"
      contract: "Enforces input/output sandboxing, privilege boundaries, and prompt injection filters"
    - skill: "devops-engineering"
      contract: "Deploys subagent runners in isolated, unprivileged containers with hard timeouts"
lazy_references:
  - file: "references/subagent-dag-decomposition.md"
    condition: "Activated when designing parallel agent workflows, dependency graphs, topological sorting, or fan-out/fan-in synthesis"
  - file: "references/mcp-tool-schema-design.md"
    condition: "Activated when defining Model Context Protocol tool contracts, JSON Schema Draft 2020-12, or Pydantic tool models"
  - file: "references/context-compaction-memory.md"
    condition: "Activated when managing token budgets, rolling summaries, sliding window buffers, or episodic state checkpoints"
  - file: "references/adversarial-prompt-guardrails.md"
    condition: "Activated when defending against indirect prompt injection, securing tool output pipelines, or enforcing Dual-LLM privilege isolation"
  - file: "references/spec-driven-and-trajectory-evals.md"
    condition: "Activated when building Spec-Driven agent harnesses, preventing phantom velocity, or scoring DAG tool-call trajectories"
---

# Agentic AI & Multi-Agent Orchestration Skill

Authoritative knowledge base, canonical architectures, and production guidelines synthesizing standards from:
- **Model Context Protocol (MCP) Specification** — [MCP Tool Schema & Protocol Reference](./references/mcp-tool-schema-design.md)
- **Multi-Agent Directed Acyclic Graph (DAG) Topologies** — [Subagent DAG Decomposition Reference](./references/subagent-dag-decomposition.md)
- **Autonomous Agent Memory & Token Economics** — [Context Compaction & Episodic Memory Reference](./references/context-compaction-memory.md)
- **Agentic AI Security & Guardrails** — [Adversarial Prompt Guardrails Reference](./references/adversarial-prompt-guardrails.md)
- **Spec-Driven Harnesses & Trajectory Evals** — [Spec-Driven & Trajectory Evals Reference](./references/spec-driven-and-trajectory-evals.md)

---

## 1. Multi-Agent DAG Orchestration Topology

When orchestrating complex workflows across specialized subagents, avoid unstructured prompt chains. Model workflows as a **Directed Acyclic Graph ($G = (V, E)$)**:
1. **Nodes ($V$)**: Immutable units of specialized work (e.g., *Researcher*, *Backend Engineer*, *AppSec Auditor*, *Verifier*).
2. **Directed Edges ($E$)**: Data dependency contracts ($U \rightarrow V$ indicates $V$ requires artifacts from $U$).
3. **Execution Engine**:
   - Order execution via **Kahn's Topological Sort Algorithm**.
   - Validate acyclicity prior to dispatch via 3-color Depth-First Search (`WHITE`, `GRAY`, `BLACK`) cycle detection.
   - Execute independent subgraphs in parallel (**Fan-Out**).
   - Aggregate multi-agent findings at synchronization join points (**Fan-In**) with configurable quorum thresholds ($\ge 80\%$ success).

---

## 2. Model Context Protocol (MCP) Tool Contract Standard

Tools exposed to autonomous agents must adhere strictly to **JSON-RPC 2.0** and **JSON Schema Draft 2020-12**:
- **Root Requirement**: The `inputSchema` must be an object (`type: "object"`) containing explicit `properties` and `required` arrays.
- **SSRF Hardening**: MCP implementations must forbid dynamic resolution of external `$ref` network URIs.
- **Idempotency**: Every state-mutating tool call requires an explicit client-generated `idempotency_key: str (UUIDv4)`.
- **Output Contracts**: Pair `inputSchema` with an explicit `outputSchema` so downstream LLM parsing is deterministic and verifiable.

---

## 3. Sliding-Window Token Budgeting & Context Compaction

To protect agent cognitive performance and prevent **Context Rot** and the **Lost-in-the-Middle** trap:
- **Pinned System Prefix**: Fixed system instructions, identity, and tool definitions protected with cache breakpoints.
- **Threshold-Triggered Compaction**: When conversational context reaches $\ge 75\%$ of the designated token budget, trigger an automated compaction routine.
- **High-Entropy State Retention**: Preserve high-information tokens (architectural decisions, file paths, active diffs, error stack traces); compress verbose intermediate reasoning into structured handoff snapshots.
- **Episodic Persistence**: Write completed subtasks and settled decisions to `.agent/memory/project_state.schema.json`.

---

## 4. Dual-LLM Pattern & Adversarial Guardrails

To defend against **Indirect Prompt Injection** from untrusted external sources (web content, user uploads, third-party tool outputs):
- **Quarantined Worker (Untrusted)**: Ingests raw external content with **zero tools and zero system execution permissions**. Outputs sanitized JSON summaries.
- **Privileged Controller (Trusted)**: Receives sanitized abstractions from deterministic controller code. Holds execution tools (file write, terminal, database). Never parses raw external content directly.
- **Plan-Then-Execute Invariant**: The privileged agent locks a static execution plan before dispatching subagents. Intermediate untrusted tool returns cannot alter the execution graph dynamically.
