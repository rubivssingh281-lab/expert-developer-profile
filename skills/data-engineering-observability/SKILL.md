---
name: data-engineering-observability
description: >-
  Use this skill when designing modern lean data pipelines (Apache Iceberg, Polars, DuckDB), implementing durable execution workflows (Temporal), or instrumenting unified OpenTelemetry (OTel) distributed tracing, metrics, logs, and AI/LLM telemetry.
trigger_patterns:
  keywords: ["iceberg", "polars", "duckdb", "parquet", "arrow", "temporal", "durable execution", "opentelemetry", "otel", "tracing", "data pipeline", "lakehouse", "etl", "elt", "llm telemetry"]
  file_globs: ["**/*pipeline*.py", "**/*workflow*.py", "**/*etl*.py", "**/*telemetry*.py", "**/*otel*.py", "**/*duckdb*.py"]
  architectural_intents: ["lean-data-pipeline", "lakehouse-storage", "durable-workflow-execution", "distributed-tracing-otel", "agentic-telemetry"]
theta_bindings:
  governing_parameters: ["sigma", "delta"]
  parameter_mappings:
    sigma:
      local-edge: "Embedded DuckDB + Polars lazy frames on local Parquet/Iceberg files, console OTel exporter"
      startup-1k-rps: "Polars + DuckDB single-node workers, S3-backed Apache Iceberg tables, OTel collector to Grafana/Prometheus"
      growth-10k-rps: "Temporal durable workflow orchestration, Iceberg partitioning & compaction, full OTel traceparent + LLM token telemetry"
      hyperscale-100k-rps: "Multi-engine Iceberg lakehouse (Trino/Spark/DuckDB), Temporal multi-namespace clusters, sampled OTel tail-based pipelines"
cross_skill_hooks:
  upstream:
    - skill: "agentic-orchestration"
      contract: "Wraps long-running multi-step agent loops in Temporal durable workflows and emits OTel GenAI spans"
  downstream:
    - skill: "fastapi-backend-architecture"
      contract: "Propagates W3C traceparent headers and serves low-latency analytical aggregates via DuckDB/Parquet"
    - skill: "devops-engineering"
      contract: "Deploys OTel Collector DaemonSets, Prometheus/Tempo/Loki stacks, and Temporal server Helm charts"
lazy_references:
  - file: "references/iceberg-polars-duckdb-stack.md"
    condition: "Activated when processing tabular datasets, Parquet/Iceberg lakehouse storage, zero-copy Arrow transforms, or embedded analytics"
  - file: "references/temporal-durable-execution-otel.md"
    condition: "Activated when designing failure-proof durable workflows with Temporal or instrumenting OpenTelemetry distributed + LLM telemetry"
---

# Data Engineering, Durable Execution & Unified Observability Skill

Authoritative knowledge base and production patterns synthesizing modern data & reliability architectures:
- **The Lean Open Lakehouse Stack** — [Apache Iceberg, Polars & DuckDB Reference](./references/iceberg-polars-duckdb-stack.md)
- **Resilient State & Telemetry** — [Temporal Durable Execution & OpenTelemetry Reference](./references/temporal-durable-execution-otel.md)

---

## 1. Core Architectural Philosophy: "Not Every Problem Deserves a Cluster"

Modern data engineering rejects premature distributed Spark cluster overhead:
1. **Decoupled Open Storage (Apache Iceberg)**: Store tables once in cloud object storage (`S3`/`GCS`) with ACID transactions, hidden partitioning, and time-travel. Read concurrently from DuckDB, Polars, Trino, or Snowflake without vendor lock-in.
2. **Vectorized Single-Node Compute (Polars & DuckDB)**: Use Rust-backed **Polars** (`LazyFrame` + Apache Arrow) and embedded **DuckDB** to process tens of gigabytes in seconds on a single node before ever considering distributed clusters.
3. **Durable Execution (Temporal)**: Wrap multi-step API ingestion, retries, and stateful AI agent pipelines in **Temporal Workflows** so crashes resume seamlessly from the exact checkpoint line.
4. **Unified Telemetry (OpenTelemetry)**: Close the **Agentic Visibility Gap** by capturing metrics, logs, HTTP traces, and LLM token/latency/prompt spans in one vendor-neutral OTel pipeline.
