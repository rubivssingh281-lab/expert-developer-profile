# Temporal Durable Execution & Unified OpenTelemetry (OTel) Observability

Authoritative manual for eliminating fragile retry boilerplate with Temporal durable workflows and closing the Agentic Visibility Gap with OpenTelemetry semantic instrumentation.

---

## 1. Durable Execution with Temporal

Traditional cron scripts and message queues lose execution state if a worker node restarts mid-pipeline. **Temporal** separates deterministic orchestration (**Workflows**) from side-effecting I/O (**Activities**), automatically persisting event history so interrupted execution resumes from the exact step without duplicate side effects:

```python
from __future__ import annotations

from datetime import timedelta
from temporalio import activity, workflow
from temporalio.common import RetryPolicy

@activity.defn
async def fetch_external_records(batch_id: str) -> list[str]:
    # Non-deterministic I/O (API call, LLM invocation, DB write) runs inside Activities
    return [f"record-{batch_id}-1", f"record-{batch_id}-2"]

@activity.defn
async def write_iceberg_batch(records: list[str]) -> int:
    return len(records)

@workflow.defn
class IngestionPipelineWorkflow:
    @workflow.run
    async def run(self, batch_id: str) -> int:
        policy = RetryPolicy(
            initial_interval=timedelta(seconds=2),
            backoff_coefficient=2.0,
            maximum_attempts=5,
        )
        records = await workflow.execute_activity(
            fetch_external_records,
            batch_id,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=policy,
        )
        written = await workflow.execute_activity(
            write_iceberg_batch,
            records,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=policy,
        )
        return written
```

---

## 2. Unified OpenTelemetry (OTel) & Closing the Agentic Visibility Gap

When autonomous AI agents execute tools, query RAG stores, and call downstream microservices, every span must carry unified OTel context (`traceparent`) plus standardized GenAI semantic attributes:

```python
from __future__ import annotations

from opentelemetry import trace

tracer = trace.get_tracer("agentic.platform", "3.0.0")

def trace_llm_tool_step(
    agent_name: str,
    model_id: str,
    prompt_tokens: int,
    completion_tokens: int,
) -> None:
    """Emits standardized OpenTelemetry GenAI span attributes to close agentic blind spots."""
    with tracer.start_as_current_span(f"agent.step.{agent_name}") as span:
        span.set_attribute("gen_ai.system", "vllm")
        span.set_attribute("gen_ai.request.model", model_id)
        span.set_attribute("gen_ai.usage.input_tokens", prompt_tokens)
        span.set_attribute("gen_ai.usage.output_tokens", completion_tokens)
        span.set_attribute("agent.actor_id", agent_name)
```

### Mandatory Telemetry Consolidation Checklist
- **Unified OTLP Pipeline**: Route application traces, structured JSON logs (`trace_id`, `span_id`), RED/USE metrics, and LLM token/cost telemetry through a single OpenTelemetry Collector.
- **Actor Attribution**: Tag every mutating operation with both authenticated human `user_id` and autonomous `agent.actor_id` to audit agent-initiated changes.
- **DORA Integration**: Derive Deployment Frequency, Lead Time for Changes, MTTR, and Change Failure Rate directly from CI/CD and OTel trace metadata.
