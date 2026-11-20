# Subagent DAG Decomposition & Multi-Agent Execution Topologies

Authoritative engineering manual for designing, validating, and executing deterministic multi-agent Directed Acyclic Graphs (DAGs) in production AI agent systems.

---

## 1. Formal Mathematical Model of an Agent DAG

A multi-agent workflow is formalized as a Directed Acyclic Graph $G = (V, E)$:
- **Vertices** (`V = {v_1, v_2, ..., v_n}`): Distinct agent execution tasks with specified subagent persona, input schema, tool access permissions, and output contract.
- **Edges ($E \subseteq V \times V$)**: Directed data and precedence constraints. A directed edge $(u, v) \in E$ denotes that agent $v$ depends on the output of agent $u$ and cannot begin execution until $u$ completes successfully.
- **Acyclicity Invariant**: For all paths `p = (v_1, v_2, ..., v_k)`, `v_1 != v_k`. The graph contains strictly zero cycles.

---

## 2. Definition-Time Cycle Detection & Kahn's Topological Sort

Before any agent task is scheduled or dispatched to an execution runtime, the orchestrator must validate graph acyclicity and compute the execution order.

### Kahn's Algorithm Implementation in Python
```python
from __future__ import annotations
from collections import defaultdict, deque
from typing import Generic, TypeVar, Hashable

T = TypeVar("T", bound=Hashable)

class CycleDetectedError(Exception):
    """Raised when a circular dependency is detected in an agent execution graph."""

class AgentDAG(Generic[T]):
    def __init__(self) -> None:
        self.adj_list: dict[T, list[T]] = defaultdict(list)
        self.in_degree: dict[T, int] = defaultdict(int)
        self.nodes: set[T] = set()

    def add_node(self, node: T) -> None:
        self.nodes.add(node)
        if node not in self.in_degree:
            self.in_degree[node] = 0

    def add_edge(self, upstream: T, downstream: T) -> None:
        self.add_node(upstream)
        self.add_node(downstream)
        self.adj_list[upstream].append(downstream)
        self.in_degree[downstream] += 1

    def topological_sort(self) -> list[T]:
        """Computes a valid linear execution order via Kahn's algorithm.
        Raises CycleDetectedError if a cycle exists.
        """
        in_deg = dict(self.in_degree)
        queue: deque[T] = deque([node for node in self.nodes if in_deg[node] == 0])
        ordered: list[T] = []

        while queue:
            current = queue.popleft()
            ordered.append(current)

            for neighbor in self.adj_list[current]:
                in_deg[neighbor] -= 1
                if in_deg[neighbor] == 0:
                    queue.append(neighbor)

        if len(ordered) != len(self.nodes):
            unresolved = set(self.nodes) - set(ordered)
            raise CycleDetectedError(f"Circular dependency detected involving nodes: {unresolved}")

        return ordered
```

---

## 3. Parallel Dispatch & Synchronization (Fan-Out / Fan-In)

When multiple agent nodes have in-degree $0$ or have all prerequisites resolved, they can be executed concurrently in asynchronous worker pools.

```text
               ┌──> [ Backend Agent ] ──────┐
               │                            │
[ Planner ] ───┼──> [ Security Agent ] ─────┼──> [ Synthesizer / Verifier ]
               │                            │
               └──> [ SRE / DevOps Agent ] ─┘
                   (Fan-Out: Parallel)           (Fan-In: Quorum Merge)
```

### Async Parallel Dispatcher with Quorum Merging
```python
import asyncio
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class AgentResult:
    node_id: str
    success: bool
    payload: dict[str, Any]
    error: str | None = None

async def execute_fan_out_fan_in(
    tasks: list[tuple[str, Any]],
    timeout_seconds: float = 30.0,
    quorum_ratio: float = 0.80,
) -> list[AgentResult]:
    """Dispatches agent tasks in parallel and synchronizes results using quorum thresholds."""
    
    async def run_single(node_id: str, coro: Any) -> AgentResult:
        try:
            res = await asyncio.wait_for(coro, timeout=timeout_seconds)
            return AgentResult(node_id=node_id, success=True, payload=res)
        except Exception as exc:
            return AgentResult(node_id=node_id, success=False, payload={}, error=str(exc))

    results: list[AgentResult] = await asyncio.gather(
        *(run_single(node_id, coro) for node_id, coro in tasks)
    )

    success_count = sum(1 for r in results if r.success)
    actual_ratio = success_count / len(tasks) if tasks else 1.0

    if actual_ratio < quorum_ratio:
        failed_nodes = [r.node_id for r in results if not r.success]
        raise RuntimeError(
            f"Fan-in quorum failed: {actual_ratio:.1%} < {quorum_ratio:.1%}. Failed nodes: {failed_nodes}"
        )

    return results
```

---

## 4. Runtime Deadlock & Straggler Prevention

Even if a graph is structurally acyclic, runtime deadlocks occur if subagents block indefinitely waiting on shared external resources, rate-limited APIs, or locked database rows.

### Mandatory Operational Protections:
1. **Per-Node Timeout Envelope**: Every subagent invocation must declare an explicit `timeout_seconds`. Never invoke `await subagent.run()` without a timeout context.
2. **Exponential Backoff with Full Jitter**: If a subagent encounters a transient rate limit (HTTP 429 / 503), retry with randomized exponential backoff:
   $$t_{\text{sleep}} = \text{Uniform}(0, \min(t_{\text{max}}, t_{\text{base}} \times 2^{\text{attempt}}))$$
3. **Dead-Letter Handoff**: If an agent node exceeds its maximum retry threshold, route the execution state to a fallback node or alert the parent orchestrator with a structured error payload.
