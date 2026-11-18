#!/usr/bin/env bash
# ==============================================================================
# Maker/Checker Split & Git Worktree Parallel Harness
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

usage() {
    echo "Usage:"
    echo "  bash maker_checker_loop.sh --create-worktree <task_slug>"
    echo "  bash maker_checker_loop.sh --verify-worktree <task_slug>"
    echo "  bash maker_checker_loop.sh --cleanup-worktree <task_slug>"
    exit 1
}

if [[ $# -lt 2 ]]; then
    usage
fi

ACTION="$1"
TASK_SLUG="$2"
WORKTREE_DIR="${REPO_ROOT}/../wt-${TASK_SLUG}"
BRANCH_NAME="agent/${TASK_SLUG}"

case "${ACTION}" in
    --create-worktree)
        echo "[HARNESS] Creating isolated worktree for task: ${TASK_SLUG}"
        git worktree add "${WORKTREE_DIR}" -b "${BRANCH_NAME}"
        echo "[HARNESS] Worktree ready at: ${WORKTREE_DIR}"
        ;;
    --verify-worktree)
        echo "[CHECKER] Initiating adversarial falsification in: ${WORKTREE_DIR}"
        if [[ ! -d "${WORKTREE_DIR}" ]]; then
            echo "[CHECKER] Error: Worktree directory does not exist: ${WORKTREE_DIR}" >&2
            exit 1
        fi
        pushd "${WORKTREE_DIR}" > /dev/null
        echo "[CHECKER] Running deterministic integrity validation..."
        python3 scripts/validate_repo_integrity.py --check-math --check-sync
        echo "[CHECKER] Running blueprint verification..."
        bash templates/hooks/verify_blueprint.sh
        popd > /dev/null
        echo "[CHECKER] PASSED: Worktree ${TASK_SLUG} certified by Checker persona."
        ;;
    --cleanup-worktree)
        echo "[HARNESS] Cleaning up worktree: ${WORKTREE_DIR}"
        git worktree remove "${WORKTREE_DIR}" --force
        git branch -D "${BRANCH_NAME}" || true
        echo "[HARNESS] Cleanup complete."
        ;;
    *)
        usage
        ;;
esac
