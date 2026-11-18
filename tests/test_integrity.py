"""Pytest suite for repository brain integrity and synchronization."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()

def test_validate_repo_integrity_script() -> None:
    """Asserts that scripts/validate_repo_integrity.py exits with 0."""
    script_path = REPO_ROOT / "scripts" / "validate_repo_integrity.py"
    assert script_path.exists(), "validate_repo_integrity.py must exist"

    result = subprocess.run(
        [sys.executable, str(script_path), "--check-math", "--check-sync"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Integrity check failed: {result.stderr or result.stdout}"

def test_context_compactor_validation() -> None:
    """Asserts that context_compactor.py validates state cleanly."""
    script_path = REPO_ROOT / "scripts" / "context_compactor.py"
    assert script_path.exists(), "context_compactor.py must exist"

    result = subprocess.run(
        [sys.executable, str(script_path), "--validate-only"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Compactor validation failed: {result.stderr or result.stdout}"
