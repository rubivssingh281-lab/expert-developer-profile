# Lean Data Lakehouse: Apache Iceberg, Polars & DuckDB

Authoritative manual for building high-throughput, zero-cluster-overhead data pipelines using Apache Arrow memory semantics, Polars lazy execution, DuckDB SQL analytics, and Apache Iceberg open tables.

---

## 1. Polars Lazy Execution (`LazyFrame`)

Unlike eager Pandas execution (which materializes intermediate copies and struggles with single-core GIL limits), **Polars** builds a query plan and applies predicate/projection pushdown before multithreaded Rust execution:

```python
from __future__ import annotations

import polars as pl

def transform_events_lazy(input_glob: str, output_parquet: str, min_amount: float) -> None:
    """Streams Parquet files lazily with predicate pushdown and zero-copy Arrow output."""
    lf = (
        pl.scan_parquet(input_glob)
        .filter(pl.col("status") == "SETTLED")
        .filter(pl.col("amount_usd") >= min_amount)
        .with_columns(
            pl.col("event_ts").dt.truncate("1h").alias("hour_bucket"),
        )
        .group_by(["tenant_id", "hour_bucket"])
        .agg(
            pl.col("amount_usd").sum().alias("hourly_revenue_usd"),
            pl.len().alias("tx_count"),
        )
    )
    # Streaming sink avoids OOM on datasets larger than host RAM
    lf.sink_parquet(output_parquet, compression="zstd")
```

---

## 2. DuckDB In-Process Analytical Engine

DuckDB acts as *"SQLite for Analytics"*, executing vectorized columnar SQL directly against Parquet and Apache Iceberg tables in S3/GCS or local storage, and seamlessly powering CI/CD data quality tests:

```python
from __future__ import annotations

import duckdb

def query_iceberg_snapshot(iceberg_metadata_path: str, tenant_id: str) -> list[tuple[str, float]]:
    """Queries an Apache Iceberg table directly without an external data warehouse."""
    with duckdb.connect(database=":memory:") as conn:
        conn.execute("INSTALL iceberg; LOAD iceberg;")
        rows = conn.execute(
            """
            SELECT hour_bucket::TEXT, hourly_revenue_usd
            FROM iceberg_scan(?)
            WHERE tenant_id = ?
            ORDER BY hour_bucket DESC
            LIMIT 24
            """,
            [iceberg_metadata_path, tenant_id],
        ).fetchall()
    return [(str(r[0]), float(r[1])) for r in rows]
```

---

## 3. Apache Iceberg Best Practices

| Capability | Operational Standard |
| :--- | :--- |
| **ACID & Time-Travel** | Pin analytical reads to snapshot IDs for deterministic ML feature reproducibility (`AS OF SYSTEM TIME`). |
| **Hidden Partitioning** | Define `days(event_ts)` transforms in table metadata so analysts never write brittle manual partition filters. |
| **Small-File Compaction** | Schedule periodic `rewrite_data_files` maintenance to compact streaming micro-batches into optimal 128–512 MB Parquet files. |
| **Catalog Governance** | Use an open REST Catalog (Polaris / Lakekeeper / Unity) so multiple engines share atomic table commits safely. |
