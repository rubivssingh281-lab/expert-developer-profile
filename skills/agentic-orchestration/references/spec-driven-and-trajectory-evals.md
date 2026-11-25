# Spec-Driven Development, Engineering Agent Harnesses & DAG Trajectory Evals

Authoritative manual for governing autonomous coding agents with executable specifications, deterministic harnesses, and trajectory-level DAG verification.

---

## 1. Spec-Driven Development & Engineering Agent Harnesses

Autonomous coding agents fail catastrophically when given vague prompts without structural guardrails. Pair **Spec-Driven Development** with an **Agent Harness**:
1. **Executable Spec Before Code**: Author explicit Pydantic/OpenAPI contracts, JSON Schemas, and test assertions *before* invoking code generation agents.
2. **Agent Harness Enforcement**: Wrap agent runs in deterministic pre/post-commit verification (`ruff`, `mypy --strict`, `bandit`, `pytest`, and integrity linters) so generated code cannot accumulate silent technical debt or security regressions (*anti-phantom-velocity*).
3. **Scoped Least-Privilege Environments**: Execute agent tool calls inside ephemeral git worktrees or sandboxed containers with explicit path/network allowlists.

---

## 2. DAG Trajectory & Tool-Call Evaluation

Evaluating only an agent's final response hides looping failures, wasted tokens, and unsafe intermediate tool calls. Score the complete **Execution Trajectory DAG**:

```python
from __future__ import annotations

from pydantic import BaseModel

class TrajectoryStep(BaseModel):
    step_id: str
    tool_name: str
    valid_schema: bool
    latency_ms: float
    recovered_from_error: bool = False

def evaluate_agent_trajectory(
    steps: list[TrajectoryStep],
    expected_tools: list[str],
    max_steps: int = 12,
) -> dict[str, float | bool]:
    """Scores tool selection accuracy, schema compliance, and loop safety across an agent run."""
    invoked = [s.tool_name for s in steps]
    tool_recall = len(set(expected_tools) & set(invoked)) / max(len(expected_tools), 1)
    schema_rate = sum(1 for s in steps if s.valid_schema) / max(len(steps), 1)
    loop_safe = len(steps) <= max_steps
    return {
        "tool_recall": round(tool_recall, 3),
        "schema_compliance": round(schema_rate, 3),
        "loop_safe": loop_safe,
        "passed": tool_recall == 1.0 and schema_rate == 1.0 and loop_safe,
    }
```

### Mandatory Agentic Observability Attributes
- Record `agent.step_index`, `agent.tool_name`, `agent.retry_count`, and `gen_ai.usage.*` on every OpenTelemetry span to eliminate the **Agentic Visibility Gap**.
