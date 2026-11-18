# Autonomous Incident & Architecture Remediation Playbook

**Target Service**: `{{ service_name }}`  
**Scale Tier**: `{{ scale_tier }}`  
**Security Posture**: `{{ security_posture }}`  
**Compute Envelope**: `{{ compute_envelope }}`  
**Symptom**: `{{ symptom_class }}`  

---

## 1. Automated Diagnostic Runbook

{% if symptom_class == "db_pool_exhaustion" %}
### Symptom Analysis: Database Pool Saturation
Executing Postgres inspection queries to isolate connection leakage:

```sql
-- 1. Identify long-running idle in transaction sessions
SELECT pid, usename, client_addr, state, age(clock_timestamp(), state_change) as duration, query
FROM pg_stat_activity
WHERE state = 'idle in transaction'
ORDER BY duration DESC
LIMIT 10;

-- 2. Inspect active locks and blocked processes
SELECT blocked_locks.pid     AS blocked_pid,
       blocking_locks.pid    AS blocking_pid,
       blocked_activity.query AS blocked_statement,
       blocking_activity.query AS blocking_statement
FROM  pg_catalog.pg_locks         blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks         blocking_locks 
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
    AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
    AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
    AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
    AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
    AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
    AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

**Immediate Action**: Terminate blocking sessions over 60s:
```sql
SELECT pg_terminate_backend(pid) FROM pg_stat_activity 
WHERE state = 'idle in transaction' AND age(clock_timestamp(), state_change) > interval '60 seconds';
```

{% elif symptom_class == "oom_kill" %}
### Symptom Analysis: OOM Kill / Memory Threshold Overrun
Executing memory boundary audit against `{{ compute_envelope }}`:

```bash
# 1. Inspect Linux cgroup OOM events
dmesg -T | grep -i oom-killer | tail -n 20

# 2. Inspect active VRAM allocation
nvidia-smi --query-gpu=memory.total,memory.used,memory.free --format=csv
```

**Immediate Action**:
- Reduce dynamic micro-batch queue size by 50% in `app.state`.
- Enable 4-bit `nf4` QLoRA quantization and VAE latents tiling.

{% elif symptom_class == "p99_latency_spike" %}
### Symptom Analysis: P99 Tail Latency Degradation
Executing concurrency and threadpool starvation checks:

```bash
# Check event loop lag and thread pool utilization
curl -s http://localhost:8000/metrics | grep -E "fastapi_requests_duration_seconds|process_resident_memory_bytes"
```

**Immediate Action**:
- Enable shed load via LIFO queue rejection (`503 Service Unavailable`).
- Evict expired keys from local cache.
{% endif %}

---

## 2. Quantitative Verification Gate (`[CAPACITY_MATH]`)

```math
L_{\text{concurrency}} = \lambda_{\text{RPS}} \times W_{\text{P99LatencySec}} \le \text{QueueCapacity}_{\text{max}}
```

- Assert `P99 < 250ms` and `ErrorRate < 0.01%` over a 5-minute stabilization window before resolving incident.
