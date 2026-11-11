#!/usr/bin/env bash
# ==============================================================================
# Installer for Expert Developer Profile (Antigravity & AI Agents)
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
    echo "Usage:"
    echo "  bash install.sh --global               # Install globally to ~/.gemini/config/"
    echo "  bash install.sh --project /path/to/dir # Install into a specific project (.agents/)"
    exit 1
}

if [[ $# -eq 0 ]]; then
    usage
fi

case "$1" in
    --global)
        TARGET_DIR="${HOME}/.gemini/config"
        echo "Installing Expert Developer Profile globally to: ${TARGET_DIR}"
        mkdir -p "${TARGET_DIR}/skills" "${TARGET_DIR}/templates"
        cp -v "${SCRIPT_DIR}/GEMINI.md" "${TARGET_DIR}/GEMINI.md"
        cp -rv "${SCRIPT_DIR}/skills/"* "${TARGET_DIR}/skills/"
        cp -rv "${SCRIPT_DIR}/templates/"* "${TARGET_DIR}/templates/"
        echo "✅ Global installation complete!"
        ;;
    --project)
        if [[ -z "${2:-}" ]]; then
            echo "Error: Missing target project directory path."
            usage
        fi
        PROJECT_DIR="$2"
        TARGET_DIR="${PROJECT_DIR}/.agents"
        echo "Installing Expert Developer Profile into project: ${PROJECT_DIR}"
        mkdir -p "${TARGET_DIR}/skills" "${TARGET_DIR}/templates"
        cp -v "${SCRIPT_DIR}/AGENTS.md" "${TARGET_DIR}/AGENTS.md"
        cp -rv "${SCRIPT_DIR}/skills/"* "${TARGET_DIR}/skills/"
        cp -rv "${SCRIPT_DIR}/templates/"* "${TARGET_DIR}/templates/"
        echo "✅ Project installation complete!"
        ;;
    *)
        usage
        ;;
esac
