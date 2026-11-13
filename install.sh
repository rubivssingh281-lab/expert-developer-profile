#!/usr/bin/env bash
# ==============================================================================
# Installer for Expert Developer Profile (v2.0 Parameterized Agent Brain)
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
    echo "Usage:"
    echo "  bash install.sh --global [--profile <default|blitz|fortress|vram8|vram24|hyperscale>]"
    echo "  bash install.sh --project /path/to/dir [--profile <profile>] [--enable-pre-commit]"
    echo ""
    echo "Profiles:"
    echo "  default      - Full Principal Architect cognitive profile (tau=3, sigma=growth-10k-rps, rho=zero-trust-public, kappa=gpu-24gb-vram, delta=full-blueprint)"
    echo "  blitz        - Rapid hotfix / prototyping profile (tau=1, sigma=local-edge, rho=internal-prod, kappa=cpu-only, delta=surgical-diff)"
    echo "  fortress     - Maximum AppSec hardening & red-team audit profile (tau=4, sigma=growth-10k-rps, rho=zero-trust-public, kappa=cpu-only, delta=red-team-audit)"
    echo "  vram8        - 8GB VRAM ML profile (tau=3, sigma=local-edge, rho=internal-prod, kappa=gpu-8gb-vram, delta=full-blueprint)"
    echo "  vram24       - 24GB VRAM ML production serving profile (tau=3, sigma=startup-1k-rps, rho=zero-trust-public, kappa=gpu-24gb-vram, delta=full-blueprint)"
    echo "  hyperscale   - 100k+ RPS distributed HA & multi-node FSDP profile (tau=4, sigma=hyperscale-100k-rps, rho=zero-trust-public, kappa=multi-node-fsdp, delta=full-blueprint)"
    exit 1
}

MODE=""
TARGET_DIR=""
PROJECT_DIR=""
PROFILE="default"
ENABLE_PRE_COMMIT=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --global)
            MODE="global"
            TARGET_DIR="${HOME}/.gemini/config"
            shift
            ;;
        --project)
            MODE="project"
            if [[ -z "${2:-}" || "${2:-}" =~ ^-- ]]; then
                echo "Error: Missing path for --project" >&2
                usage
            fi
            PROJECT_DIR="$2"
            TARGET_DIR="${PROJECT_DIR}/.agents"
            shift 2
            ;;
        --profile)
            if [[ -z "${2:-}" ]]; then
                echo "Error: Missing profile argument" >&2
                usage
            fi
            PROFILE="$2"
            shift 2
            ;;
        --enable-pre-commit)
            ENABLE_PRE_COMMIT=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown argument: $1" >&2
            usage
            ;;
    esac
done

if [[ -z "${MODE}" ]]; then
    usage
fi

echo "🚀 Installing Expert Developer Profile (v2.0 Parameterized Brain)..."
echo "📦 Installation Mode: ${MODE}"
echo "🎯 Target Directory: ${TARGET_DIR}"
echo "⚙️  Selected Profile: ${PROFILE}"

# 1. Create directory structure
mkdir -p "${TARGET_DIR}/skills" "${TARGET_DIR}/templates" "${TARGET_DIR}/memory"

# 2. Copy instruction rules
if [[ "${MODE}" == "global" ]]; then
    cp -v "${SCRIPT_DIR}/GEMINI.md" "${TARGET_DIR}/GEMINI.md"
else
    cp -v "${SCRIPT_DIR}/AGENTS.md" "${TARGET_DIR}/AGENTS.md"
fi

# 3. Copy all 5 domain skills
echo "📚 Synchronizing 5 Core Domain Skills..."
cp -rv "${SCRIPT_DIR}/skills/"* "${TARGET_DIR}/skills/"

# 4. Copy templates and verification hooks
echo "🏗️ Synchronizing Production Templates & Verification Hooks..."
cp -rv "${SCRIPT_DIR}/templates/"* "${TARGET_DIR}/templates/"
chmod +x "${TARGET_DIR}/templates/hooks/verify_blueprint.sh" 2>/dev/null || true

# 5. Initialize episodic memory state
echo "🧠 Initializing Episodic Memory Schema & ADR Ledger..."
if [[ -d "${SCRIPT_DIR}/.agent/memory" ]]; then
    cp -rv "${SCRIPT_DIR}/.agent/memory/"* "${TARGET_DIR}/memory/"
fi

# 6. Configure Git Pre-Commit Hook if requested
if [[ "${ENABLE_PRE_COMMIT}" == true && -n "${PROJECT_DIR}" ]]; then
    if [[ -d "${PROJECT_DIR}/.git" ]]; then
        echo "🔗 Linking verify_blueprint.sh into ${PROJECT_DIR}/.git/hooks/pre-commit..."
        mkdir -p "${PROJECT_DIR}/.git/hooks"
        ln -sf "${TARGET_DIR}/templates/hooks/verify_blueprint.sh" "${PROJECT_DIR}/.git/hooks/pre-commit"
        chmod +x "${PROJECT_DIR}/.git/hooks/pre-commit"
        echo "✅ Pre-commit verification hook configured!"
    else
        echo "⚠️  No .git directory found in ${PROJECT_DIR}; skipping git hook configuration."
    fi
fi

echo ""
echo "=============================================================================="
echo "✅ Expert Developer Profile (v2.0) successfully installed to: ${TARGET_DIR}"
echo "Activated 5 Core Skills:"
echo "  1. Devops & Cloud Infrastructure (Kubernetes, BuildKit, SRE, Terraform)"
echo "  2. Cybersecurity & Application Security (NIST CSF 2.0, OWASP, PortSwigger)"
echo "  3. AI/ML & LLM Systems Engineering (PyTorch FSDP2, PEFT, Scikit-Learn, vLLM)"
echo "  4. FastAPI & Distributed Backend (FastAPI, PostgreSQL 18, Martin Fowler PoEAA)"
echo "  5. Agentic AI & Multi-Agent Orchestration (MCP, Subagent DAGs, Dual-LLM Guardrails)"
echo "=============================================================================="
