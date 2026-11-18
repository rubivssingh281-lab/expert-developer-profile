#!/usr/bin/env bash
# ==============================================================================
# Installer for Expert Developer Profile (v3.0 Parameterized Agent Brain)
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
    echo "Usage:"
    echo "  bash install.sh --global [--profile <profile>] [--harness <all|antigravity|gemini|claude|cursor|copilot>]"
    echo "  bash install.sh --project /path/to/dir [--profile <profile>] [--harness <harness>] [--enable-pre-commit]"
    echo ""
    echo "Profiles:"
    echo "  default      - Full Principal Architect cognitive profile (tau=3, sigma=growth-10k-rps, rho=zero-trust-public, kappa=gpu-8gb-vram)"
    echo "  blitz        - Rapid hotfix / prototyping profile (tau=1, sigma=local-edge, rho=internal-prod, kappa=cpu-only, delta=surgical-diff)"
    echo "  fortress     - Maximum AppSec hardening & red-team audit profile (tau=4, rho=regulated-pci-hipaa, delta=adversarial-verifier)"
    echo "  vram8        - 8GB VRAM ML profile (tau=3, sigma=local-edge, rho=internal-prod, kappa=gpu-8gb-vram)"
    echo "  vram24       - 24GB VRAM ML production serving profile (tau=3, sigma=startup-1k-rps, kappa=gpu-24gb-vram)"
    echo "  hyperscale   - 100k+ RPS distributed HA & multi-node FSDP profile (tau=4, sigma=hyperscale-100k-rps, kappa=multi-node-fsdp2)"
    echo ""
    echo "Harness Targets:"
    echo "  all          - Install rules and configurations for all agent platforms (default)"
    echo "  antigravity  - Install Antigravity GEMINI.md & skills/ config"
    echo "  gemini       - Install Gemini CLI rules"
    echo "  claude       - Install Claude Code CLAUDE.md"
    echo "  cursor       - Install Cursor .cursor/rules/expert-architect.mdc"
    echo "  copilot      - Install GitHub Copilot .github/copilot-instructions.md"
    exit 1
}

MODE=""
TARGET_DIR=""
PROJECT_DIR=""
PROFILE="default"
HARNESS="all"
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
            TARGET_DIR="${PROJECT_DIR}"
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
        --harness)
            if [[ -z "${2:-}" ]]; then
                echo "Error: Missing harness argument" >&2
                usage
            fi
            HARNESS="$2"
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

echo "🚀 Installing Expert Developer Profile (v3.0 Parameterized Brain & Harness)..."
echo "📦 Installation Mode: ${MODE}"
echo "🎯 Target Directory: ${TARGET_DIR}"
echo "⚙️  Selected Profile: ${PROFILE}"
echo "🤖 Selected Harness: ${HARNESS}"

mkdir -p "${TARGET_DIR}"

# 1. Copy Harness Rule Files
if [[ "${HARNESS}" == "all" || "${HARNESS}" == "antigravity" || "${HARNESS}" == "gemini" ]]; then
    echo "Installing GEMINI.md..."
    cp -v "${SCRIPT_DIR}/GEMINI.md" "${TARGET_DIR}/GEMINI.md"
fi

if [[ "${HARNESS}" == "all" || "${HARNESS}" == "claude" ]]; then
    echo "Installing CLAUDE.md..."
    cp -v "${SCRIPT_DIR}/CLAUDE.md" "${TARGET_DIR}/CLAUDE.md"
fi

if [[ "${HARNESS}" == "all" ]]; then
    echo "Installing AGENTS.md..."
    cp -v "${SCRIPT_DIR}/AGENTS.md" "${TARGET_DIR}/AGENTS.md"
fi

if [[ "${HARNESS}" == "all" || "${HARNESS}" == "cursor" ]]; then
    echo "Installing Cursor rules..."
    mkdir -p "${TARGET_DIR}/.cursor/rules"
    cp -v "${SCRIPT_DIR}/.cursor/rules/expert-architect.mdc" "${TARGET_DIR}/.cursor/rules/"
fi

if [[ "${HARNESS}" == "all" || "${HARNESS}" == "copilot" ]]; then
    echo "Installing GitHub Copilot instructions..."
    mkdir -p "${TARGET_DIR}/.github"
    cp -v "${SCRIPT_DIR}/.github/copilot-instructions.md" "${TARGET_DIR}/.github/"
fi

# 2. Copy 5 domain skills
echo "📚 Synchronizing 5 Core Domain Skills..."
mkdir -p "${TARGET_DIR}/skills"
cp -rv "${SCRIPT_DIR}/skills/"* "${TARGET_DIR}/skills/"

# 3. Copy templates, scripts & memory
echo "🏗️ Synchronizing Production Templates & Verification Hooks..."
mkdir -p "${TARGET_DIR}/templates" "${TARGET_DIR}/scripts" "${TARGET_DIR}/.agent/memory"
cp -rv "${SCRIPT_DIR}/templates/"* "${TARGET_DIR}/templates/"
cp -rv "${SCRIPT_DIR}/scripts/"* "${TARGET_DIR}/scripts/"
cp -rv "${SCRIPT_DIR}/.agent/memory/"* "${TARGET_DIR}/.agent/memory/"

chmod +x "${TARGET_DIR}/templates/hooks/"*.sh 2>/dev/null || true
chmod +x "${TARGET_DIR}/scripts/"*.py 2>/dev/null || true

# 4. Configure Git Pre-Commit Hook if requested
if [[ "${ENABLE_PRE_COMMIT}" == true && -n "${PROJECT_DIR}" ]]; then
    if [[ -d "${PROJECT_DIR}/.git" ]]; then
        echo "🔗 Linking verify_blueprint.sh into ${PROJECT_DIR}/.git/hooks/pre-commit..."
        mkdir -p "${PROJECT_DIR}/.git/hooks"
        ln -sf "${TARGET_DIR}/templates/hooks/verify_blueprint.sh" "${PROJECT_DIR}/.git/hooks/pre-commit"
        chmod +x "${PROJECT_DIR}/.git/hooks/pre-commit"
        echo "✅ Pre-commit verification hook configured!"
    fi
fi

# 5. Run post-install integrity check if python3 available
if command -v python3 >/dev/null 2>&1; then
    echo "🧪 Running post-install integrity verification..."
    python3 "${TARGET_DIR}/scripts/validate_repo_integrity.py" --check-math --check-sync
fi

echo ""
echo "=============================================================================="
echo "✅ Expert Developer Profile (v3.0) successfully installed to: ${TARGET_DIR}"
echo "=============================================================================="
