# Model Context Protocol (MCP) & Agent2Agent (A2A v1.0) Architecture

Authoritative engineering manual for building, securing, and deploying enterprise-grade Model Context Protocol (MCP) servers and Agent2Agent (A2A v1.0) distributed multi-agent swarms.

---

## 1. Model Context Protocol (MCP) Specification

The Model Context Protocol establishes a standardized client-server boundary between host agent harnesses and execution capabilities across 5 distinct primitives:
1. **Prompts**: Parameterized reusable prompts registered on the server.
2. **Resources**: Structured file, data, or context streams read by the agent.
3. **Tools**: Executable functions with Pydantic v2 JSON Schema input validation.
4. **Sampling**: Nested sub-model generation delegation.
5. **Roots**: Filesystem root boundary declarations.

### 1.1 Transport Protocol & Streaming Fallback
- Primary transport: **Streamable HTTP (`/mcp`)** using standard HTTP `POST` requests for JSON-RPC 2.0 payloads.
- Streaming transport: **Server-Sent Events (SSE)** at `/mcp/events` for long-running tool execution progress notifications.
- Local transport: **Standard I/O (`stdio`)** for sub-process isolated tools.

### 1.2 Tool Annotations & Safety Hints
Every MCP tool schema must expose explicit safety hints to the host agent:
- `readOnlyHint`: Boolean flag asserting zero side-effects.
- `destructiveHint`: Boolean flag asserting permanent state mutation (triggers HITL cryptographic confirmation).
- `idempotentHint`: Boolean asserting identical outcome on repeated calls with identical parameters.
- `openWorldHint`: Boolean indicating whether the tool interacts with untrusted external networks.

---

## 2. Agent2Agent (A2A v1.0) Interoperability Standard

While MCP connects agents to tools and resources vertically, A2A v1.0 connects autonomous agents horizontally across network and trust boundaries.

### 2.1 Agent Card Discovery Schema (`/.well-known/agent.json`)
Every A2A-compliant agent node exposes its capabilities via `GET /.well-known/agent.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "name": "ExpertArchitectWorker",
  "version": "1.0.0",
  "url": "https://agent-node.internal.net/a2a",
  "description": "Autonomous Staff Engineer agent for backend architecture and code generation",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false,
    "statePersistence": true
  },
  "authentication": {
    "type": "oauth2",
    "authorizationUrl": "https://auth.internal.net/oauth2/authorize",
    "tokenUrl": "https://auth.internal.net/oauth2/token",
    "scopes": {
      "a2a:tasks:submit": "Submit asynchronous tasks",
      "a2a:tasks:read": "Inspect task execution status and logs"
    }
  },
  "skills": [
    {
      "id": "fastapi-backend-architecture",
      "version": "3.0.0"
    },
    {
      "id": "aiml-engineering",
      "version": "3.0.0"
    }
  ]
}
```

### 2.2 Task Lifecycle State Machine
A2A tasks transition through a deterministic finite-state automaton:
1. `submitted`: Task accepted and assigned UUIDv7 ID.
2. `working`: Agent is executing subagent DAG or tool chains.
3. `input-required`: Agent requires clarification or approval (HITL).
4. `completed`: Terminal state; artifacts and receipts delivered.
5. `failed`: Terminal state; error details returned via RFC 9457 format.
6. `canceled`: Terminal state; explicitly revoked by caller.

---

## 3. Python MCP-to-A2A Adapter Pattern

```python
from __future__ import annotations

import httpx
from typing import Any
from pydantic import BaseModel, Field

class A2ATaskSubmission(BaseModel):
    task_id: str
    target_agent_url: str
    intent: str
    input_payload: dict[str, Any]

class MCPtoA2ABridge:
    """Invokes remote A2A agents from an MCP server environment."""
    def __init__(self, http_client: httpx.AsyncClient, bearer_token: str) -> None:
        self.client = http_client
        self.token = bearer_token

    async def dispatch_task(self, submission: A2ATaskSubmission) -> dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Idempotency-Key": submission.task_id,
        }
        payload = {
            "jsonrpc": "2.0",
            "method": "tasks/send",
            "params": {
                "id": submission.task_id,
                "intent": submission.intent,
                "input": submission.input_payload,
            },
            "id": 1,
        }
        resp = await self.client.post(
            f"{submission.target_agent_url}/tasks/send",
            headers=headers,
            json=payload,
            timeout=30.0,
        )
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result
```
