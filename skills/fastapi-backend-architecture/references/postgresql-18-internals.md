# PostgreSQL 18 Production Architecture & Internals Reference

Synthesized from **PostgreSQL 18 Official Documentation Manual & Internal Architecture**.

---

## 1. PostgreSQL 18 Cutting-Edge Architectural Upgrades

### A. Native Asynchronous I/O (AIO) Subsystem
- **Mechanism**: Replaces synchronous blocking disk reads with an event-driven asynchronous I/O framework powered by `io_uring` on modern Linux kernels.
- **Impact**: Up to $3\times$ faster throughput on sequential scans, bitmap heap scans, and background autovacuum passes by pre-fetching and overlapping concurrent page reads.
- **Observability**: `EXPLAIN (ANALYZE, BUFFERS)` now exposes async I/O wait times and pre-fetched block metrics.

### B. B-Tree "Skip Scan" Index Lookups
- Historically, if an index was created on `(tenant_id, created_at, status)` and a query filtered only on `created_at` and `status`, PostgreSQL could not use the index and fell back to a full sequential table scan.
- **Skip Scan** allows the query engine to jump between unique values of the leading column, making composite indexes reusable across queries that omit the leading column:
```sql
-- Composite index
CREATE INDEX idx_tenant_orders ON orders (tenant_id, created_at, status);

-- In PostgreSQL 18, this query uses idx_tenant_orders via Skip Scan
-- even though tenant_id is NOT in the WHERE clause:
SELECT * FROM orders WHERE status = 'COMPLETED' AND created_at >= NOW() - INTERVAL '7 days';
```

### C. Native `uuidv7()` Timestamp-Clustered UUIDs
- `uuidv4()` generates random 128-bit values, causing severe B-Tree index page splits and cache churn.
- `uuidv7()` encodes a Unix millisecond timestamp into the high-order bits:
  ```sql
  CREATE TABLE events (
      id UUID PRIMARY KEY DEFAULT uuidv7(),
      payload JSONB NOT NULL
  );
  ```
- **Advantage**: Guaranteed monotonic B-Tree insertion locality—combines the sequential write performance of auto-incrementing integers with the global uniqueness and distributed generation safety of UUIDs.

---

## 2. Advanced Indexing Strategies

### GIN on JSONB (`jsonb_path_ops`)
```sql
CREATE INDEX idx_audit_meta ON audit_logs USING gin (metadata jsonb_path_ops);
```
- `jsonb_path_ops` indexes only the hash of each path and value, resulting in index sizes up to $60\%$ smaller than default `jsonb_ops` and significantly faster `@>` containment lookups.

### BRIN (Block Range Index)
- For multi-gigabyte or terabyte append-only tables physically ordered by timestamp:
```sql
CREATE INDEX idx_sensor_readings_time ON sensor_readings USING brin (recorded_at);
```
- A BRIN index stores only the min/max values per range of disk blocks. An index on 100M rows can take $< 500 \text{ KB}$ of memory instead of $2 \text{ GB}$ for a B-tree.

---

## 3. Concurrency, MVCC & Transaction Isolation
PostgreSQL implements Multi-Version Concurrency Control (MVCC):
- Every tuple contains `xmin` (creating transaction ID) and `xmax` (deleting/updating transaction ID).
- An `UPDATE` does not overwrite the row in place; it writes a new version of the row and marks `xmax` on the old row.

### Query Profiling with EXPLAIN (ANALYZE, BUFFERS)
```sql
EXPLAIN (ANALYZE, BUFFERS, SETTINGS, WAL)
SELECT * FROM orders WHERE status = 'PENDING' AND total > 500;
```
Checklist:
- `Buffers: shared hit=... read=...`: `hit` means served from RAM (`shared_buffers`); high `read` indicates disk I/O bottlenecks.
- `Rows Removed by Filter`: High count indicates a missing index.
- `Planning Time` vs `Execution Time`.

---

## 4. High Availability & Logical Replication Architecture

### A. Logical Replication Failover
Historically, promoting a physical standby broke all downstream logical subscriptions because replication slot progress was not mirrored.
- **Failover-Enabled Subscriptions**:
  ```sql
  CREATE SUBSCRIPTION analytics_sub 
  CONNECTION 'host=primary_db port=5432 dbname=prod' 
  PUBLICATION core_data 
  WITH (failover = true);
  ```
- **Slot Synchronization Configuration**:
  - Standby setting: `sync_replication_slots = true` ensures slots stay continuously mirrored on standbys.
  - Primary setting: `synchronized_standby_slots = 'physical_standby_1'` ensures WAL sender processes hold until physical replicas have acknowledged receipt.

### B. `pg_createsubscriber` Tool
- Converts an existing physical streaming standby into a logical replica (subscriber) pointing at a publisher.
- Eliminates the massive performance penalty, WAL generation, and table sync lock contention of running a full initial table `COPY` over logical replication.
