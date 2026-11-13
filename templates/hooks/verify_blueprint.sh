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

# --- 1. Python Code Quality & Static Typing Gates ---
echo ""
echo "--- [1/4] Auditing Python Blueprints ---"

PYTHON_FILES=$(find "${REPO_ROOT}/templates" "${REPO_ROOT}/skills" -name "*.py" 2>/dev/null || true)

if [[ -n "${PYTHON_FILES}" ]]; then
    if command -v ruff >/dev/null 2>&1; then
        echo "Running ruff check..."
        if ! ruff check ${PYTHON_FILES}; then
            record_failure "ruff static analysis reported issues."
        else
            record_success "ruff check passed."
        fi
    else
        echo "⚠️  ruff not installed in current environment; skipping ruff check."
    fi

    if command -v mypy >/dev/null 2>&1; then
        echo "Running mypy --strict..."
        if ! mypy --strict ${PYTHON_FILES}; then
            record_failure "mypy --strict type checking failed."
        else
            record_success "mypy --strict passed."
        fi
    else
        echo "⚠️  mypy not installed in current environment; skipping mypy check."
    fi

    if command -v bandit >/dev/null 2>&1; then
        echo "Running bandit -r security analysis..."
        if ! bandit -r ${PYTHON_FILES} -ll -ii; then
            record_failure "bandit security scan flagged high/medium risks."
        else
            record_success "bandit security scan passed."
        fi
    else
        echo "⚠️  bandit not installed in current environment; skipping bandit check."
    fi
else
    echo "No python files found in target search path."
fi

# --- 2. Secret Scanning & Zero Placeholder Audit ---
echo ""
echo "--- [2/4] Auditing Secrets & Code Hygiene Invariants ---"

# Check for accidental hardcoded private keys or tokens
SECRET_MATCHES=$(grep -rnE '(PRIVATE KEY-----|AKIA[0-9A-Z]{16}|ghp_[0-9a-zA-Z]{36})' "${REPO_ROOT}/templates" "${REPO_ROOT}/skills" 2>/dev/null || true)
if [[ -n "${SECRET_MATCHES}" ]]; then
    record_failure "Potential secret or private key found in repository:\n${SECRET_MATCHES}"
else
    record_success "Zero raw cryptographic secrets detected."
fi

# Check for unresolved placeholders in production blueprints
PLACEHOLDER_MATCHES=$(grep -rnE '(\bTODO\b|\bFIXME\b|\bXXX\b|\.\.\.\s*$)' "${REPO_ROOT}/templates" 2>/dev/null || true)
if [[ -n "${PLACEHOLDER_MATCHES}" ]]; then
    record_failure "Unresolved placeholders (TODO/FIXME/...) detected in templates/:\n${PLACEHOLDER_MATCHES}"
else
    record_success "Zero placeholders detected in production blueprints."
fi

# --- 3. Dockerfile Container Hardening Audit ---
echo ""
echo "--- [3/4] Auditing Container Security & BuildKit Directives ---"

DOCKERFILES=$(find "${REPO_ROOT}/templates" -name "Dockerfile*" 2>/dev/null || true)

for df in ${DOCKERFILES}; do
    echo "Evaluating Dockerfile: ${df}"

    # Verify non-root execution
    if ! grep -qE '^USER\s+(10001|appuser|[1-9][0-9]{3,})' "${df}"; then
        record_failure "${df} does not enforce non-root user execution (missing 'USER 10001' or unprivileged UID)."
    else
        record_success "${df} enforces unprivileged non-root execution."
    fi

    # Verify BuildKit syntax directive
    if ! head -n 5 "${df}" | grep -q "syntax=docker/dockerfile"; then
        record_failure "${df} missing '# syntax=docker/dockerfile:1' BuildKit directive."
    else
        record_success "${df} declares BuildKit syntax specification."
    fi
done

# --- 4. Kubernetes Manifest Architecture & SecurityContext Audit ---
echo ""
echo "--- [4/4] Auditing Kubernetes Manifest Security Contexts ---"

K8S_MANIFESTS=$(find "${REPO_ROOT}/templates/kubernetes" -name "*.yaml" -o -name "*.yml" 2>/dev/null || true)

for mf in ${K8S_MANIFESTS}; do
    echo "Evaluating Kubernetes Manifest: ${mf}"

    # Verify SecurityContext invariants
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

        # Verify resource requests and limits are defined
        if ! grep -q "resources:" "${mf}" || ! grep -q "limits:" "${mf}" || ! grep -q "requests:" "${mf}"; then
            record_failure "${mf} missing explicit resource requests and limits."
        else
            record_success "${mf} defines complete resource requests and limits."
        fi
    fi
done

echo ""
echo "=============================================================================="
if [[ ${FAILURES} -gt 0 ]]; then
    echo "❌ Architectural Verification FAILED with ${FAILURES} violation(s)." >&2
    exit 1
else
    echo "✅ Deterministic Architectural Verification PASSED with zero violations!"
    exit 0
fi
