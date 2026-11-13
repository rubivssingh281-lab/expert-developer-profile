#!/usr/bin/env bash
# ==============================================================================
# 4-Commit Sequential Execution & Push Script for Expert Developer Profile v2.0
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"

echo "🚀 Starting 4-Commit Sequential Execution in ${REPO_ROOT}..."

# Verify git repository
if [[ ! -d ".git" ]]; then
    echo "Error: Not a git repository!" >&2
    exit 1
fi

# Ensure user credentials if not set
if ! git config user.name >/dev/null 2>&1; then
    git config user.name "rubivssingh281-lab"
fi
if ! git config user.email >/dev/null 2>&1; then
    git config user.email "rubivssingh281@gmail.com"
fi

# ------------------------------------------------------------------------------
# Commit 1: Meta-Cognitive Control Plane & Parameterized Brain Core
# ------------------------------------------------------------------------------
echo ""
echo "📦 [1/4] Staging and committing Parameterized Brain Core..."
git add GEMINI.md AGENTS.md AntigravityMasterUpgradePrompt.md
git commit -m "feat: v2.0 cognitive brain upgrade with theta-vector control and 6-stage meta-cognitive loop" || echo "Nothing new to commit for Commit 1."

# ------------------------------------------------------------------------------
# Commit 2: 5th Core Skill (Agentic Orchestration) & YAML Frontmatter Refactor
# ------------------------------------------------------------------------------
echo ""
echo "📦 [2/4] Staging and committing Agentic Orchestration Skill & YAML Frontmatter..."
git add \
    skills/aiml-engineering/SKILL.md \
    skills/cybersecurity-appsec/SKILL.md \
    skills/devops-engineering/SKILL.md \
    skills/fastapi-backend-architecture/SKILL.md \
    skills/agentic-orchestration/
git commit -m "feat: add agentic-orchestration skill and refactor all skills with machine-parseable YAML frontmatter" || echo "Nothing new to commit for Commit 2."

# ------------------------------------------------------------------------------
# Commit 3: Episodic Memory Architecture & Hardened Operational Templates
# ------------------------------------------------------------------------------
echo ""
echo "📦 [3/4] Staging and committing Episodic Memory & Hardened Operational Templates..."
git add \
    .agent/memory/ \
    templates/hooks/verify_blueprint.sh \
    templates/fastapi-pytorch-service/main.py \
    templates/checklists/PR_ARCHITECTURE_SECURITY_CHECKLIST.md
git commit -m "feat: implement episodic memory schema, verification hooks, and unified 4-skill service blueprint" || echo "Nothing new to commit for Commit 3."

# ------------------------------------------------------------------------------
# Commit 4: Multi-Profile Installer, Documentation Index & Release Packaging
# ------------------------------------------------------------------------------
echo ""
echo "📦 [4/4] Staging and committing Multi-Profile Installer & Release Index..."
git add \
    install.sh \
    README.md \
    scripts/commit_all.sh
git commit -m "feat: update multi-profile installer and documentation index for v2.0 parameterized release" || echo "Nothing new to commit for Commit 4."

echo ""
echo "=============================================================================="
echo "✅ All 4 commits successfully executed!"
git log -n 4 --oneline
echo "=============================================================================="

# Optional Push to Remote Origin
DO_PUSH=false
if [[ "${1:-}" == "--push" || "${1:-}" == "-p" ]]; then
    DO_PUSH=true
fi

if [[ "${DO_PUSH}" == true ]]; then
    echo ""
    echo "🚀 Pushing commits to GitHub (origin/main)..."
    git push origin main
    echo "🎉 Successfully pushed to GitHub!"
else
    echo ""
    echo "💡 To push to GitHub, run:"
    echo "   git push origin main"
    echo "   (or run this script with --push)"
fi
