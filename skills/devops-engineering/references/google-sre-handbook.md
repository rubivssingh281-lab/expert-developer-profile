# Google Site Reliability Engineering (SRE) Handbook

Synthesized from **Google Site Reliability Engineering (SRE) Book & Workbook**.

---

## 1. SLI, SLO, and SLA Mathematics

### Definitions
- **SLI (Service Level Indicator)**: The quantifiable ratio of good events to total events:
  $$\text{SLI} = \frac{\text{Good Events}}{\text{Total Events}} \times 100\%$$
  *Example:* $\frac{\text{Count of HTTP responses with status } < 500 \text{ and latency } \le 250\text{ms}}{\text{Total HTTP requests}}$
- **SLO (Service Level Objective)**: Target percentage over a specific rolling window (typically 30 days):
  $$\text{SLO} = 99.9\% \text{ over 30 days}$$
- **SLA (Service Level Agreement)**: Legal contract specifying financial penalties if SLO is violated. SREs engineer against SLOs, not SLAs.

### Error Budget & Burn Rate
$$\text{Error Budget} = 100\% - \text{SLO}$$
* For $99.9\%$ SLO: Error Budget is $0.1\% = 0.001$.
* Over a 30-day window ($43,200$ minutes), an allowed downtime is:
  $$43,200 \times 0.001 = 43.2 \text{ minutes}$$

**Burn Rate Formula**:
$$\text{Burn Rate} = \frac{\text{Actual Error Rate}}{\text{Allowed Error Rate}}$$
* A burn rate of $1$ consumes $100\%$ of the budget in exactly 30 days.
* A burn rate of $14.4$ consumes $2\%$ of the 30-day budget in 1 hour (Critical alert trigger!).

---

## 2. Toil Elimination Framework
Toil is operational work that exhibits these five traits:
1. **Manual** (typing commands, moving files)
2. **Repetitive** (done over and over)
3. **Automatable** (could be scripted by software)
4. **Tactical** (interrupt-driven, short-term fix)
5. **No enduring value** (system does not improve after work is completed)

**SRE 50% Rule**: If an engineer spends $\ge 50\%$ of time on toil, product feature velocity stalls and operational instability escalates. Allocate minimum $50\%$ engineering time strictly to building automation, improving resilience, and writing software.

---

## 3. Cascading Failure Prevention (Chapter 22)
Cascading failure occurs when a localized failure increases load on surviving instances, causing them to collapse sequentially.

### Defensive Engineering Patterns
1. **LIFO (Last-In, First-Out) Queue Scheduling Under Overload**:
   - When incoming request rates exceed backend processing capacity, standard FIFO queues cause latency to skyrocket.
   - Requests sitting deep in a FIFO queue have often already timed out on the client side; processing them is wasted CPU.
   - Under overload, switch queuing to LIFO so newly arriving requests (which still have valid client deadlines) succeed, preserving goodput while shedding expired requests.
2. **Deadline Propagation**:
   - Every incoming request must carry a deadline timeout (e.g., `X-Request-Deadline: 500ms`).
   - Propagate this deadline across all downstream RPC / microservice calls. If a downstream service detects the deadline has already passed, it aborts immediately rather than executing unnecessary computation.
3. **Exponential Backoff with Full Jitter**:
   $$\text{Sleep} = \text{random}(0, \min(M, B \times 2^{\text{attempt}}))$$
   Without jitter, retrying clients synchronize their requests, producing massive traffic spikes that hammer recovering servers (thundering herd).
4. **Load Shedding**:
   - Reject unprioritized traffic at the ingress gateway (returning HTTP 503 early and cheaply) when CPU, memory, or thread pool exceeds safe operating capacity.

---

## 4. Blameless Post-Mortem Standard
Post-mortems are cultural and technical instruments to eliminate recurring failure classes.

### Post-Mortem Structure
```markdown
# Incident Post-Mortem: [Service Name] - [Date]

## Executive Summary
- Duration: [Start Time] to [End Time] (Total: X minutes)
- User Impact: X% of user requests returned 502 Bad Gateway
- Revenue/SLO Budget Consumed: X% of monthly error budget

## Timeline (All times in UTC)
- 14:02 - Canary deployment of v2.4.1 started.
- 14:08 - Prometheus alert fired: Error rate > 2%.
- 14:12 - Incident Commander declared SEV-1.
- 14:18 - Rollback executed to v2.4.0.
- 14:23 - Error rates recovered to baseline (<0.01%).

## Root Cause Analysis
- Immediate Cause: Unindexed foreign key in migration #42 caused full table scans, exhausting PostgreSQL connection pool.
- Underlying Systemic Factor: CI staging environment had only 500 rows; production query planner switched to sequential scan with 12M rows.

## Lessons Learned
- What went well: Alert fired within 6 minutes; rollback executed without data corruption.
- Where we got lucky: Canary was restricted to 10% traffic.

## Action Items (Prioritized & Assigned)
1. [P0] Add synthetic load testing with production-scale row counts in CI [Owner: DevSecOps]
2. [P1] Add pre-merge query linting checking for unindexed foreign keys [Owner: Database Team]
```
