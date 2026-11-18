# Model Context Protocol (MCP) Tool Schema Design & Engineering Guide

Authoritative technical standard for defining, validating, and serving tools via the **Model Context Protocol (MCP)** using **JSON-RPC 2.0** and **JSON Schema Draft 2020-12**.

---

## 1. JSON-RPC 2.0 Protocol Foundation

All MCP client-server communication complies strictly with the JSON-RPC 2.0 specification:
- **Requests**: Contain `"jsonrpc": "2.0"`, an alphanumeric `id`, a `method` string, and structured `params`.
- **Responses**: Contain `"jsonrpc": "2.0"`, the identical `id`, and either a `result` dictionary or an `error` object.
- **Notifications**: Requests without an `id` field representing one-way telemetry; the receiver must not respond.

### Standard JSON-RPC Error Payload Format
```json
{
  "jsonrpc": "2.0",
  "id": "req-9876",
  "error": {
    "code": -32602,
    "message": "Invalid params: feature vector dimension must be exactly 10",
    "data": {
      "field": "features",
      "expected_length": 10,
      "received_length": 8
    }
  }
}
```

---

## 2. Tool Definition Protocol (`tools/list`)

When a client queries available tools using the `tools/list` method, the server responds with an array of tool descriptors. Every tool requires an `inputSchema` of `type: "object"`.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "execute_model_inference",
        "description": "Submits a normalized 10-dimensional tensor vector for batch classification with audit logging.",
        "inputSchema": {
          "$schema": "https://json-schema.org/draft/2020-12/schema",
          "type": "object",
          "properties": {
            "idempotency_key": {
              "type": "string",
              "format": "uuid",
              "description": "Unique UUIDv4 idempotency key preventing duplicate processing on retries."
            },
            "tenant_id": {
              "type": "string",
              "format": "uuid",
              "description": "Cryptographically authenticated tenant UUID."
            },
            "features": {
              "type": "array",
              "items": { "type": "number" },
              "minItems": 10,
              "maxItems": 10,
              "description": "10-dimensional float feature vector."
            }
          },
          "required": ["idempotency_key", "tenant_id", "features"],
          "additionalProperties": false
        },
        "outputSchema": {
          "$schema": "https://json-schema.org/draft/2020-12/schema",
          "type": "object",
          "properties": {
            "record_id": { "type": "string", "format": "uuid" },
            "predicted_class": { "type": "integer" },
            "confidence": { "type": "number" }
          },
          "required": ["record_id", "predicted_class", "confidence"],
          "additionalProperties": false
        }
      }
    ]
  }
}
```

---

## 3. Pydantic v2 Contract Generation Pattern

Generate production MCP `inputSchema` definitions directly from typed Pydantic models with `model_config = ConfigDict(extra="forbid", strict=True)`.

```python
from __future__ import annotations
from typing import Annotated
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class MCPInferenceInput(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        str_strip_whitespace=True,
    )

    idempotency_key: UUID = Field(
        description="Unique UUIDv4 idempotency key preventing duplicate execution on network retries."
    )
    tenant_id: UUID = Field(
        description="Authenticated tenant owner ID enforcing authorization boundaries."
    )
    features: list[float] = Field(
        min_length=10,
        max_length=10,
        description="Exactly 10 normalized float features for deep inference."
    )

def generate_mcp_input_schema() -> dict:
    """Generates a Draft 2020-12 compliant JSON schema for MCP tool registration."""
    schema = MCPInferenceInput.model_json_schema()
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    return schema
```

---

## 4. MCP Security & Protocol Invariants

1. **Forbid Network `$ref` Resolution**:
   - To mitigate Server-Side Request Forgery (SSRF) and prompt injection via external schema inclusion, MCP server runtimes must completely disable network resolution of external `$ref` URIs.
2. **Deterministic Output Serialization**:
   - Tool execution returns must be serialized using strict JSON (`additionalProperties: false`) rather than unstructured free-form text strings, enabling downstream verification tools to validate types before re-injecting into the model context.
3. **Idempotency Guarantee**:
   - Every mutation must check the `idempotency_key` against a fast-lookup key-value cache (Redis) before executing state changes:
     ```python
     if not await redis.set(f"idemp:{key}", "LOCKED", nx=True, ex=300):
         # Return cached response or raise 409 Conflict
         return await fetch_existing_result(key)
     ```
