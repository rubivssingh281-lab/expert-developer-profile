# Autonomous Agent Context Compaction & Episodic Memory Architecture

Authoritative engineering manual for managing long-horizon token economics, sliding window budgets, rolling compaction, and episodic memory persistence for autonomous coding agents.

---

## 1. The Context Saturation Problem: Rot vs. Retention

Iterative agent loops (such as ReAct loops executing compiler feedback, file edits, and tool calls) face two distinct constraints:
1. **Quadratic Cost & Latency Escalation**: Re-processing growing historical turns across dozens of iterations results in quadratic token consumption and unacceptable time-to-first-token.
2. **Context Rot & "Lost-in-the-Middle"**: Filling active context with verbose build logs, trial-and-error stack traces, and repetitive file readings degrades attention precision, causing models to violate foundational system invariants established in early turns.

---

## 2. Tiered Memory Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. Pinned System Prefix (Immutable System Rules & Prompts)   │ <-- Protected with Cache Breakpoints
├─────────────────────────────────────────────────────────────┤
│ 2. Sliding Active Window (Recent 4-8 Dialogue / Tool Turns) │ <-- High-frequency rolling buffer
├─────────────────────────────────────────────────────────────┤
│ 3. Compacted State Ledger (Distilled Milestone Summaries)   │ <-- Triggered at 75% Token Budget
├─────────────────────────────────────────────────────────────┤
│ 4. Episodic Disk Memory (`.agent/memory/project_state.json`)│ <-- Long-term structured storage
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Token Budgeting & Compaction Trigger Algorithm

Dynamic token budgeting monitors token utilization continuously. When working memory exceeds a defined capacity threshold (typically $75\%$), an automated compaction cycle executes.

### Production Compaction Routine
```python
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass
class ConversationTurn:
    role: str
    content: str
    token_count: int
    is_milestone: bool = False

class ContextCompactionEngine:
    def __init__(self, token_budget_ceiling: int = 32000, compaction_threshold: float = 0.75) -> None:
        self.ceiling = token_budget_ceiling
        self.threshold_tokens = int(token_budget_ceiling * compaction_threshold)
        self.turns: list[ConversationTurn] = []

    def total_tokens(self) -> int:
        return sum(t.token_count for t in self.turns)

    def should_compact(self) -> bool:
        return self.total_tokens() >= self.threshold_tokens

    def execute_compaction(self, compressor_llm_callable: Any) -> list[ConversationTurn]:
        """Distills turns older than the recent 4 turns into a structured state ledger."""
        if len(self.turns) <= 4:
            return self.turns

        # Retain the most recent 4 turns in the active sliding window
        retained_turns = self.turns[-4:]
        historical_turns = self.turns[:-4]

        # Extract high-entropy information into structured handoff
        distillation_prompt = (
            "Compress the following historical agent execution steps into an architectural milestone snapshot.\n"
            "Retain:\n"
            "1. Settled architectural decisions and parameter choices (theta vector).\n"
            "2. File paths modified, created, or deleted.\n"
            "3. Root causes of any resolved bugs and invariant fixes.\n"
            "Discard all raw command logs, verbose tool outputs, and trial-and-error iterations.\n\n"
            f"History:\n{[t.content for t in historical_turns]}"
        )

        compacted_summary_text = compressor_llm_callable(distillation_prompt)
        
        milestone_turn = ConversationTurn(
            role="system",
            content=f"[CONTEXT_CHECKPOINT_STATE]\n{compacted_summary_text}",
            token_count=len(compacted_summary_text) // 4,
            is_milestone=True,
        )

        self.turns = [milestone_turn] + retained_turns
        return self.turns
```

---

## 4. Episodic Memory Sync (`.agent/memory/`)

When milestones, capacity limits, or architectural trade-offs are settled, persist them to disk in `.agent/memory/project_state.schema.json` and `.agent/memory/adr_ledger_template.md`. This ensures that subsequent sessions resume with full fidelity without querying the user or re-running expensive discovery passes.
