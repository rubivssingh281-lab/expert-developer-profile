"""Integration tests for FastAPI + PyTorch production service."""

from __future__ import annotations

import pytest
from httpx import AsyncClient, ASGITransport
from pathlib import Path
import sys

# Add templates directory to path
TEMPLATES_DIR = Path(__file__).parent.parent / "templates" / "fastapi-pytorch-service"
sys.path.insert(0, str(TEMPLATES_DIR))

try:
    from main import app  # type: ignore
except ImportError:
    app = None

@pytest.mark.asyncio
async def test_health_probes() -> None:
    if app is None:
        pytest.skip("FastAPI PyTorch service dependencies not installed in test environment")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/health/live")
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("status") == "healthy"
