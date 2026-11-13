# Architectural Decision Record (ADR) Ledger Template

- **ADR ID**: `ADR-YYYYMMDD-NNN`
- **Title**: `[Short descriptive title of the architectural choice]`
- **Status**: `PROPOSED | ACCEPTED | SUPERSEDED | REJECTED`
- **Date**: `YYYY-MM-DD`
- **Governing Parameter Vector**: $\theta = \langle \tau: 3, \sigma: \text{growth-10k-rps}, \rho: \text{zero-trust-public}, \kappa: \text{gpu-24gb-vram}, \delta: \text{full-blueprint} \rangle$

---

## 1. Context & Problem Statement
Describe the engineering dilemma, workload constraints, scaling goals, and security requirements driving this decision.

---

## 2. Mandatory Quantitative Capacity Math (`[CAPACITY_MATH]`)
Concrete capacity envelopes calculated prior to candidate evaluation:
- **Database Connection Saturation**:
  $$\text{Total DB Connections} = N_{\text{pods}} \times N_{\text{uvicorn\_workers}} \times (\text{pool\_size} + \text{max\_overflow}) \le 0.80 \times \text{max\_connections}_{\text{PgBouncer/PG}}$$
- **VRAM / KV-Cache Envelope**:
  $$\text{VRAM}_{\text{total}} = M_{\text{weights}} + M_{\text{grads}} + M_{\text{optim}} + M_{\text{activations}} + M_{\text{KV-cache}} < \kappa_{\text{limit}}$$
- **SRE Little's Law Concurrency**:
  $$L = \lambda \times W_{\text{P99}}$$

---

## 3. Evaluated Candidates & Weighted Utility Score Matrix (`[WEIGHTED_ADR]`)

Utility Function:
$$U(A_k) = w_L \cdot S_{\text{Latency}}(A_k) + w_C \cdot S_{\text{Consistency}}(A_k) + w_S \cdot S_{\text{Security}}(A_k) + w_O \cdot S_{\text{OpsSimplicity}}(A_k)$$

Weights based on $\theta$: $w_L = 0.25, w_C = 0.20, w_S = 0.40, w_O = 0.15$. (Scores normalized 1–10).

| Candidate Architecture | Latency ($S_L$) | Consistency ($S_C$) | Security ($S_S$) | Ops Simplicity ($S_O$) | Total Weighted Utility $U(A_k)$ | Decision |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Candidate $A_1$: [Option 1]** | | | | | | Rejected |
| **Candidate $A_2$: [Option 2]** | | | | | | **ACCEPTED (Winner)** |
| **Candidate $A_3$: [Option 3]** | | | | | | Rejected |

---

## 4. Adversarial Red-Team & SRE Falsification Gate (`[RED_TEAM_GATE]`)
- **AppSec Attacker Perspective**: Attempted BOLA, SQLi, SSRF, and JWT bypass tests.
- **Chaos SRE Perspective**: Evaluated cascading failure risks, queue overflow under database stall, and memory leaks.

---

## 5. Consequences & Operational Follow-ups
- **Positive Consequences**:
- **Negative Consequences / Trade-offs Accepted**:
- **Downstream Actions**:
