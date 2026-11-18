# Contextual Agent Playbooks & Tools (CAPT) Architecture

Authoritative engineering manual for developing parameterized, executable Jinja2 incident and operational playbooks integrated into AI coding agent workflows.

---

## 1. The CAPT Architecture Pattern

Static markdown runbooks decay rapidly and introduce human copy-paste errors during critical incidents. The **Contextual Agent Playbooks & Tools (CAPT)** architecture transforms static runbooks into:
1. **Parameterized Jinja2 Templates**: Playbook logic defined with typed input slots and strict undefined evaluation (`StrictUndefined`).
2. **Typed MCP Tool Contracts**: Exposed directly to agents as callable tools with Pydantic v2 schemas.
3. **Deterministic Falsification Hooks**: Every rendered playbook attaches automated verification commands to prove remediation.

---

## 2. Python PlaybookRegistry Implementation

```python
from __future__ import annotations

from pathlib import Path
from typing import Any
import jinja2
from pydantic import BaseModel, ConfigDict, Field

class PlaybookContext(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    service_name: str = Field(..., description="Target service identifier")
    scale_tier: str = Field(..., description="Scale tier (e.g., growth-10k-rps)")
    security_posture: str = Field(..., description="Security tier (e.g., zero-trust-public)")
    compute_envelope: str = Field(..., description="Hardware profile (e.g., gpu-8gb-vram)")
    symptom_class: str = Field(..., description="Observed symptom: db_pool_exhaustion | oom_kill | p99_latency_spike")

class PlaybookRegistry:
    def __init__(self, templates_dir: Path) -> None:
        self.templates_dir = templates_dir
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(templates_dir)),
            undefined=jinja2.StrictUndefined,
            autoescape=False,
        )

    def render(self, template_name: str, context: PlaybookContext) -> str:
        template = self.env.get_template(template_name)
        rendered: str = template.render(**context.model_dump())
        return rendered
```

---

## 3. Operational Playbook Governance
- All playbooks must contain:
  1. Diagnostic inspection queries (`pg_stat_activity`, Linux `/proc/meminfo`, Kubernetes events).
  2. Quantitative validation of system bounds (`[CAPACITY_MATH]`).
  3. Actionable surgical mitigation commands with timeouts.
  4. Explicit rollback thresholds and verification criteria.
