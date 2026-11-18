# Context Compaction & Git Worktree Parallel Isolation

Authoritative engineering manual on preventing context rot in long-horizon AI agent sessions and executing isolated parallel agent workflows using git worktrees.

---

## 1. Context Engineering Taxonomy (arXiv:2507.13334)

Long-horizon agent execution encounters three failure modes:
1. **Context Bloat**: Intermediate tool outputs saturate the context window, causing degraded reasoning and forgotten system rules.
2. **Context Poisoning / Rot**: Hallucinated file paths or failed tool attempts in conversation history guide subsequent decisions.
3. **Working Tree Conflicts**: Multiple parallel subagents writing to shared working tree files cause overwrites and race conditions.

### The 3-Pillar Mitigation Strategy:
- **Pillar 1: Retrieval & Generation** — Lazy-load domain references only when invoked by `@mode` or `[ACTIVE_SKILLS]`.
- **Pillar 2: Processing & Compaction** — Checkpoint durable memory to `.agent/memory/STATE.md` every milestone; prune intermediate logs.
- **Pillar 3: Isolation** — Allocate private `git worktree` instances for concurrent subagent tasks.

---

## 2. Parallel Git Worktree Protocol

```bash
#!/usr/bin/env bash
set -euo pipefail

# 1. Create isolated worktree for parallel agent task
TASK_SLUG="task-fastapi-refactor"
WORKTREE_DIR="../wt-${TASK_SLUG}"
BRANCH_NAME="agent/${TASK_SLUG}"

git worktree add "${WORKTREE_DIR}" -b "${BRANCH_NAME}"

# 2. Execute isolated work in worktree directory
pushd "${WORKTREE_DIR}" > /dev/null
# Subagent executes code changes here without touching main working tree
popd > /dev/null

# 3. Clean up worktree after verification and merge
git worktree remove "${WORKTREE_DIR}" --force
```

---

## 3. Sliding-Window Compaction Receipts
When token usage approaches 65% of context window capacity, the harness invokes `context_compactor.py`:
1. Invariants from `.agent/memory/STATE.md` and `.agent/memory/PLAN.md` are evaluated.
2. Raw tool outputs are stripped.
3. A standardized `<SESSION_RESTORE_SNAPSHOT>` (<400 tokens) is returned to initialize the next agent session.
