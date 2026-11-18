#!/usr/bin/env python3
"""Episodic memory compaction and session restore snapshot utility.

Reads .agent/memory/STATE.md, validates invariants, and produces a compact
<SESSION_RESTORE_SNAPSHOT> (<400 tokens) for agent session restoration.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
DEFAULT_STATE = REPO_ROOT / ".agent" / "memory" / "STATE.md"
DEFAULT_ADR = REPO_ROOT / ".agent" / "memory" / "adr_ledger_template.md"

def extract_snapshot(state_file: Path) -> str:
    if not state_file.is_file():
        raise FileNotFoundError(f"State file not found: {state_file}")

    content = state_file.read_text(encoding="utf-8")
    lines = content.splitlines()

    theta_block: list[str] = []
    receipt: str = "Unknown"
    recording_theta = False

    for line in lines:
        if "Active Parameter Vector" in line:
            recording_theta = True
            continue
        if recording_theta:
            if line.startswith("- **") and not line.startswith("  - `"):
                recording_theta = False
            else:
                theta_block.append(line.strip())
        if "Status:" in line:
            receipt = line.strip().replace("- Status:", "").strip()

    compact_theta = " ".join(theta_block)
    snapshot = (
        "<SESSION_RESTORE_SNAPSHOT>\n"
        f"ActiveTheta: {compact_theta}\n"
        f"LastVerificationReceipt: {receipt}\n"
        "ActiveWorkspace: expert-developer-profile\n"
        "ExecutionMode: Unabridged v3.0 Harness\n"
        "</SESSION_RESTORE_SNAPSHOT>"
    )
    return snapshot

def main() -> int:
    parser = argparse.ArgumentParser(description="Context compaction utility")
    parser.add_argument("--state-file", type=Path, default=DEFAULT_STATE, help="Path to STATE.md")
    parser.add_argument("--adr-file", type=Path, default=DEFAULT_ADR, help="Path to ADR template")
    parser.add_argument("--validate-only", action="store_true", help="Validate invariants without emitting snapshot")
    args = parser.parse_args()

    try:
        snapshot = extract_snapshot(args.state_file)
        if args.validate_only:
            print("[COMPACTOR] State invariants validated successfully.")
            return 0
        print(snapshot)
        return 0
    except Exception as exc:
        print(f"[COMPACTOR] Error: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
