#!/usr/bin/env python3
"""Zero-dependency repository brain integrity, frontmatter, relative link, and MathJax linter.

Enforces:
1. All 5 core skills exist with SKILL.md and non-empty references/.
2. YAML frontmatter schema validity on all skills.
3. Internal relative markdown links resolve to existing files on disk.
4. GitHub MathJax linter: detects unescaped underscores in inline math.
5. Synchronization check: AGENTS.md, GEMINI.md, and CLAUDE.md match on rules and macros.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

REPO_ROOT = Path(__file__).parent.parent.resolve()
EXPECTED_SKILLS = [
    "agentic-orchestration",
    "aiml-engineering",
    "cybersecurity-appsec",
    "devops-engineering",
    "fastapi-backend-architecture",
]

def check_skills_completeness() -> List[str]:
    errors: List[str] = []
    skills_dir = REPO_ROOT / "skills"
    if not skills_dir.is_dir():
        return [f"Skills directory missing: {skills_dir}"]

    for skill in EXPECTED_SKILLS:
        s_dir = skills_dir / skill
        if not s_dir.is_dir():
            errors.append(f"Missing skill directory: {skill}")
            continue
        skill_md = s_dir / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"Missing SKILL.md in {skill}")
        refs_dir = s_dir / "references"
        if not refs_dir.is_dir() or not any(refs_dir.glob("*.md")):
            errors.append(f"Missing or empty references/ in {skill}")
    return errors

def check_yaml_frontmatter() -> List[str]:
    errors: List[str] = []
    skills_dir = REPO_ROOT / "skills"
    for skill in EXPECTED_SKILLS:
        skill_md = skills_dir / skill / "SKILL.md"
        if not skill_md.is_file():
            continue
        content = skill_md.read_text(encoding="utf-8")
        if not content.startswith("---"):
            errors.append(f"{skill}/SKILL.md missing opening YAML frontmatter '---'")
            continue
        parts = content.split("---", 2)
        if len(parts) < 3:
            errors.append(f"{skill}/SKILL.md missing closing YAML frontmatter '---'")
            continue
        frontmatter = parts[1]
        for required_key in ["name:", "description:"]:
            if required_key not in frontmatter:
                errors.append(f"{skill}/SKILL.md frontmatter missing required key: {required_key}")
    return errors

def check_relative_links() -> List[str]:
    errors: List[str] = []
    md_files = [
        REPO_ROOT / "README.md",
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / "GEMINI.md",
        REPO_ROOT / "CLAUDE.md",
    ]
    md_files.extend((REPO_ROOT / "skills").glob("*/SKILL.md"))

    link_regex = re.compile(r"\[([^\]]+)\]\((?!http|mailto|#)([^)]+)\)")

    for md_file in md_files:
        if not md_file.is_file():
            continue
        content = md_file.read_text(encoding="utf-8")
        for match in link_regex.finditer(content):
            target = match.group(2).split("#")[0].strip()
            if not target:
                continue
            resolved = (md_file.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"Broken relative link in {md_file.relative_to(REPO_ROOT)}: '{target}' -> {resolved} not found")
    return errors

def check_mathjax_rendering() -> List[str]:
    errors: List[str] = []
    # Match inline math $...$ that contains an underscore outside \text{...}
    # Note: We skip code blocks (```) and fenced math (```math ... ```)
    inline_math_regex = re.compile(r"(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)")

    for md_file in REPO_ROOT.rglob("*.md"):
        if ".git" in md_file.parts:
            continue
        content = md_file.read_text(encoding="utf-8")
        # Strip fenced code blocks
        clean_content = re.sub(r"```[\s\S]*?```", "", content)
        for line_num, line in enumerate(clean_content.splitlines(), start=1):
            for match in inline_math_regex.finditer(line):
                math_expr = match.group(1)
                # Check for unescaped underscore not preceded by \ or inside \text{...}
                stripped = re.sub(r"\\text\{[^}]*\}", "", math_expr)
                if "_" in stripped:
                    # Check if underscore is unescaped
                    if re.search(r"(?<!\\)_", stripped):
                        errors.append(
                            f"LaTeX error in {md_file.relative_to(REPO_ROOT)}:{line_num} "
                            f"-> Unescaped underscore in inline math: '${math_expr}$'. Use fenced ```math block instead."
                        )
    return errors

def check_root_sync() -> List[str]:
    errors: List[str] = []
    agents_path = REPO_ROOT / "AGENTS.md"
    gemini_path = REPO_ROOT / "GEMINI.md"
    claude_path = REPO_ROOT / "CLAUDE.md"

    if not agents_path.is_file() or not gemini_path.is_file() or not claude_path.is_file():
        return ["One or more root directives (AGENTS.md, GEMINI.md, CLAUDE.md) missing"]

    a_text = agents_path.read_text(encoding="utf-8")
    g_text = gemini_path.read_text(encoding="utf-8")
    c_text = claude_path.read_text(encoding="utf-8")

    expected_rules = [f"RULE-{i:02d}" for i in range(1, 8)]
    for r in expected_rules:
        if r not in a_text:
            errors.append(f"AGENTS.md missing {r}")
        if r not in g_text:
            errors.append(f"GEMINI.md missing {r}")
        if r not in c_text:
            errors.append(f"CLAUDE.md missing {r}")

    expected_macros = ["@blitz", "@fortress", "@checker", "@vram8", "@vram24", "@hyperscale", "@mcp-architect", "@rag-hybrid", "@gitops-sre", "@oss-maintainer"]
    for m in expected_macros:
        if m not in a_text:
            errors.append(f"AGENTS.md missing macro {m}")
        if m not in g_text:
            errors.append(f"GEMINI.md missing macro {m}")
        if m not in c_text:
            errors.append(f"CLAUDE.md missing macro {m}")

    return errors

def main() -> int:
    parser = argparse.ArgumentParser(description="Repository brain integrity validator")
    parser.add_argument("--check-math", action="store_true", help="Lint inline LaTeX for GitHub MathJax compliance")
    parser.add_argument("--check-sync", action="store_true", help="Verify AGENTS.md, GEMINI.md, and CLAUDE.md synchronization")
    args = parser.parse_args()

    all_errors: List[str] = []

    print("[INTEGRITY] Validating skill completeness...")
    all_errors.extend(check_skills_completeness())

    print("[INTEGRITY] Validating YAML frontmatter...")
    all_errors.extend(check_yaml_frontmatter())

    print("[INTEGRITY] Validating internal relative links...")
    all_errors.extend(check_relative_links())

    if args.check_math:
        print("[INTEGRITY] Linting LaTeX MathJax syntax...")
        all_errors.extend(check_mathjax_rendering())

    if args.check_sync:
        print("[INTEGRITY] Validating root brain directives synchronization...")
        all_errors.extend(check_root_sync())

    if all_errors:
        print(f"\n[FAIL] {len(all_errors)} integrity issue(s) detected:", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("\n[PASS] All repository integrity, skill, frontmatter, link, and synchronization checks passed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
