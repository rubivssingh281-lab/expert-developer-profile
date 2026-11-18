#!/usr/bin/env bash
# ==============================================================================
# Executable Deterministic Blueprint Verification Hook
# Staff Engineer Automated Quality, AppSec & Container Hardening Gate
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

echo "🔍 Initiating Deterministic Architectural Verification Gate..."
echo "📂 Repository Root: ${REPO_ROOT}"

FAILURES=0

record_failure() {
    local message="$1"
    echo "❌ [VERIFICATION FAILURE]: ${message}" >&2
    FAILURES=$((FAILURES + 1))
}

record_success() {
    local message="$1"
    echo "✅ [PASSED]: ${message}"
}

# --- 0. Repository Integrity, Frontmatter, Links & MathJax Linter ---
echo ""
echo "--- [0/5] Auditing Repository Integrity & Brain Synchronization ---"
if command -v python3 >/dev/null 2>&1; then
    if python3 "${REPO_ROOT}/scripts/validate_repo_integrity.py" --check-math --check-sync; then
        record_success "Repository integrity, YAML frontmatter, links, and MathJax syntax passed."
    else
        record_failure "validate_repo_integrity.py flagged issues."
    fi

    if python3 "${REPO_ROOT}/scripts/context_compactor.py" --validate-only; then
        record_success "Episodic memory state invariants validated."
    else
        record_failure "context_compactor.py state validation failed."
    fi
fi

# --- 1. Python Code Quality, Syntax AST & Static Typing Gates ---
echo ""
echo "--- [1/5] Auditing Python Blueprints & AST Syntax ---"

PYTHON_FILES=$(find "${REPO_ROOT}/templates" "${REPO_ROOT}/skills" "${REPO_ROOT}/scripts" -name "*.py" 2>/dev/null || true)

if [[ -n "${PYTHON_FILES}" ]]; then
    # Syntax check
    echo "Compiling Python AST across codebase..."
    if ! python3 -m py_compile ${PYTHON_FILES}; then
        record_failure "py_compile failed syntax compilation."
    else
        record_success "Python AST syntax compilation clean."
    fi

    if command -v ruff >/dev/null 2>&1; then
        echo "Running ruff check..."
        if ! ruff check ${PYTHON_FILES}; then
            record_failure "ruff static analysis reported issues."
        else
            record_success "ruff check passed."
        fi
    else
        echo "⚠️  ruff not installed; skipping ruff check."
    fi

    if command -v mypy >/dev/null 2>&1; then
        echo "Running mypy --strict..."
        if ! mypy --strict ${PYTHON_FILES}; then
            record_failure "mypy --strict type checking failed."
        else
            record_success "mypy --strict passed."
        fi
    else
        echo "⚠️  mypy not installed; skipping mypy check."
    fi

    if command -v bandit >/dev/null 2>&1; then
        echo "Running bandit -r security analysis..."
        if ! bandit -r ${PYTHON_FILES} -ll -ii; then
            record_failure "bandit security scan flagged high/medium risks."
        else
            record_success "bandit security scan passed."
        fi
    else
        echo "⚠️  bandit not installed; skipping bandit check."
    fi
else
    echo "No python files found in target search path."
fi

# --- 2. Secret Scanning & Zero Placeholder Audit ---
echo ""
echo "--- [2/5] Auditing Secrets & Code Hygiene Invariants ---"

SECRET_MATCHES=$(grep -rnE '(PRIVATE KEY-----|AKIA[0-9A-Z]{16}|ghp_[0-9a-zA-Z]{36})' "${REPO_ROOT}/templates" "${REPO_ROOT}/skills" 2>/dev/null || true)
if [[ -n "${SECRET_MATCHES}" ]]; then
    record_failure "Potential secret or private key found in repository:\n${SECRET_MATCHES}"
else
    record_success "Zero raw cryptographic secrets detected."
fi

PLACEHOLDER_MATCHES=$(grep -rnE '(\bTODO\b|\bFIXME\b|\bXXX\b|\.\.\.\s*$)' "${REPO_ROOT}/templates" 2>/dev/null || true)
if [[ -n "${PLACEHOLDER_MATCHES}" ]]; then
    record_failure "Unresolved placeholders detected in templates/:\n${PLACEHOLDER_MATCHES}"
else
    record_success "Zero placeholders detected in production blueprints."
fi

# --- 3. Dockerfile Container Hardening Audit ---
echo ""
echo "--- [3/5] Auditing Container Security & BuildKit Directives ---"

DOCKERFILES=$(find "${REPO_ROOT}/templates" -name "Dockerfile*" 2>/dev/null || true)

for df in ${DOCKERFILES}; do
    echo "Evaluating Dockerfile: ${df}"
    if ! grep -qE '^USER\s+(10001|appuser|[1-9][0-9]{3,})' "${df}"; then
        record_failure "${df} does not enforce non-root user execution."
    else
        record_success "${df} enforces unprivileged non-root execution."
    fi

    if ! head -n 5 "${df}" | grep -q "syntax=docker/dockerfile"; then
        record_failure "${df} missing '# syntax=docker/dockerfile:1' BuildKit directive."
    else
        record_success "${df} declares BuildKit syntax specification."
    fi
done

# --- 4. Kubernetes Manifest Architecture & SecurityContext Audit ---
echo ""
echo "--- [4/5] Auditing Kubernetes Manifest Security Contexts ---"

K8S_MANIFESTS=$(find "${REPO_ROOT}/templates/kubernetes" -name "*.yaml" -o -name "*.yml" 2>/dev/null || true)

for mf in ${K8S_MANIFESTS}; do
    echo "Evaluating Kubernetes Manifest: ${mf}"
    if grep -q "kind: Deployment" "${mf}"; then
        if ! grep -q "runAsNonRoot:\s*true" "${mf}"; then
            record_failure "${mf} missing 'runAsNonRoot: true' in securityContext."
        else
            record_success "${mf} enforces runAsNonRoot."
        fi

        if ! grep -q "readOnlyRootFilesystem:\s*true" "${mf}"; then
            record_failure "${mf} missing 'readOnlyRootFilesystem: true' in container securityContext."
        else
            record_success "${mf} enforces readOnlyRootFilesystem."
        fi
    fi
done

# --- 5. Automated Unit & Integration Tests ---
echo ""
echo "--- [5/5] Executing Test Suites ---"
if command -v pytest >/dev/null 2>&1; then
    if pytest "${REPO_ROOT}/tests" -q; then
        record_success "All pytest unit and integration test suites passed."
    else
        record_failure "pytest encountered test suite failures."
    fi
else
    echo "⚠️  pytest not installed; skipping test execution."
fi

echo ""
echo "=============================================================================="
if [[ ${FAILURES} -gt 0 ]]; then
    echo "❌ Architectural Verification FAILED with ${FAILURES} violation(s)." >&2
    exit 1
else
    echo "✅ Deterministic Architectural Verification PASSED with zero violations!"
    exit 0
fi
