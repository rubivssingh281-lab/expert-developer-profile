"""Tests for Model Context Protocol & A2A v1.0 FastAPI server."""

from __future__ import annotations

import pytest
from httpx import AsyncClient, ASGITransport
from pathlib import Path
import sys

MCP_DIR = Path(__file__).parent.parent / "templates" / "mcp-server-fastapi"
sys.path.insert(0, str(MCP_DIR))

try:
    from server import app  # type: ignore
except ImportError:
    app = None

@pytest.mark.asyncio
async def test_a2a_agent_card_discovery() -> None:
    if app is None:
        pytest.skip("MCP server dependencies not installed in test environment")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/.well-known/agent.json")
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("name") == "ExpertArchitectWorker"
        assert "skills" in data
        assert len(data["skills"]) == 5

@pytest.mark.asyncio
async def test_mcp_tools_list() -> None:
    if app is None:
        pytest.skip("MCP server dependencies not installed in test environment")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        rpc_payload = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "id": 1,
        }
        resp = await ac.post("/mcp", json=rpc_payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "result" in data
        tools = data["result"].get("tools", [])
        tool_names = [t["name"] for t in tools]
        assert "render_engineering_playbook" in tool_names
