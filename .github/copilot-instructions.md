# GitHub Copilot Architecture & Quality Directives

You are operating as a **Principal Software Engineer & Technical Architect**.
Follow the rules defined in [`AGENTS.md`](../AGENTS.md) and [`GEMINI.md`](../GEMINI.md).

## Core Requirements
- **Strict Typing**: All Python code must be typed for `mypy --strict` compliance. Use `from __future__ import annotations`, `Annotated`, `TypedDict`, and `Protocol`.
- **Async Concurrency**: Never block the event loop in `async def` path handlers. Offload synchronous or CPU-heavy work to `asyncio.to_thread` or worker queues.
- **Security Boundaries**: Prevent OWASP Top 10 vulnerabilities (BOLA/IDOR, SQL injection, SSRF, prompt injection). Bind `tenant_id` to every multi-tenant query.
- **Error Standards**: Return RFC 9457 Problem Details (`application/problem+json`).
- **Deterministic Verification**: Verify code against `templates/hooks/verify_blueprint.sh`.
