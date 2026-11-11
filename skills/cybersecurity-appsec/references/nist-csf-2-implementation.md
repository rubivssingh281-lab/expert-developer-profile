# NIST Cybersecurity Framework (CSF) 2.0 Engineering Reference

Synthesized from **NIST CSF 2.0 Official Publication & Implementation Tiers**.

---

## 1. The Six Core Functions Overview

NIST CSF 2.0 organizes cybersecurity into 6 interconnected functions. The critical addition in version 2.0 is **Govern (GV)**, which informs and guides the other five technical functions:

```text
               ┌───────────────────────┐
               │      GOVERN (GV)      │
               └───────────┬───────────┘
                           │
      ┌────────────────────┼────────────────────┐
      ▼                    ▼                    ▼
┌───────────┐        ┌───────────┐        ┌───────────┐
│ IDENTIFY  │───────►│  PROTECT  │───────►│  DETECT   │
│   (ID)    │        │   (PR)    │        │   (DE)    │
└───────────┘        └───────────┘        └─────┬─────┘
                                                │
                     ┌──────────────────────────┘
                     ▼
               ┌───────────┐        ┌───────────┐
               │  RESPOND  │───────►│  RECOVER  │
               │   (RS)    │        │   (RC)    │
               └───────────┘        └───────────┘
```

---

## 2. Function Deep-Dive & Engineering Controls

### Function 1: GOVERN (GV) — Enterprise Risk & Architecture
- **Organizational Context (`GV.OC`)**: Define regulatory posture (HIPAA, GDPR, SOC 2 Type II, PCI-DSS) and mission-critical assets.
- **Risk Management Strategy (`GV.RM`)**: Define risk appetite, thresholds for acceptable blast radius, and quantitative risk modeling.
- **Roles & Authorities (`GV.RR`)**: Segregate roles (developers do not possess direct prod database credentials; access is mediated through audited bastion/JIT systems).
- **Policy (`GV.PO`)**: Codified security policies enforced via CI linters, branch protection rules, and signed git commits.
- **Supply Chain Risk (`GV.SC`)**: Generate and cryptographically sign Software Bill of Materials (SBOM) via CycloneDX or SPDX; continuously scan dependency trees using Trivy/Snyk.

### Function 2: IDENTIFY (ID) — Asset & Threat Surface Mapping
- **Asset Inventory (`ID.AM`)**: Automated discovery of all cloud endpoints, buckets, VPCs, and serverless lambdas.
- **Threat Modeling (`ID.RA`)**: Continuous threat modeling using STRIDE during the design phase of every major backend feature.

### Function 3: PROTECT (PR) — Defensive Controls & Zero Trust
- **Identity & Access Management (`PR.AA`)**: Zero Trust architecture. No network zone is implicitly trusted. Mutual TLS (mTLS) between microservices. Enforce MFA, short-lived tokens, and least privilege IAM roles.
- **Data Security (`PR.DS`)**: Data encryption in transit (TLS 1.3) and at rest (AES-256-GCM / KMS). Zero unmasked PII in application logs.
- **Platform Hardening (`PR.PS`)**: Immutable infrastructure, distroless container images, read-only root filesystems, automated vulnerability patching.

### Function 4: DETECT (DE) — Continuous Monitoring & Telemetry
- **Continuous Monitoring (`DE.CM`)**: Aggregate structured JSON logs, system metrics, and audit trails to centralized SIEM (Elasticsearch, Splunk, Datadog).
- **Adverse Event Detection (`DE.AE`)**: Automated anomaly detection on authentication spikes, mass data export queries, and unauthorized privilege escalation attempts.

### Function 5: RESPOND (RS) — Containment & Mitigation
- **Incident Management (`RS.MA`)**: Pre-programmed automation runbooks to isolate compromised pods, revoke user sessions, and rotate compromised cloud credentials instantly.
- **Blast-Radius Containment (`RS.MI`)**: Subnet isolation, rate limiter throttling, and web application firewall (WAF) rule injections.

### Function 6: RECOVER (RC) — Resilience & Continuity
- **Restoration (`RC.RP`)**: Verified immutable, off-site backups with continuous automated restore testing. Recovery Time Objective (RTO) and Recovery Point Objective (RPO) monitoring.

---

## 3. CSF 2.0 Profiles & Implementation Tiers (NIST SP 1302)

### A. Organizational Profiles (Current vs. Target Gap Analysis)
- **Current Profile**: Documents the specific cybersecurity outcomes an organization is actively achieving today.
- **Target Profile**: Defines the desired security posture, risk thresholds, and compliance targets necessary to fulfill business goals.
- **Continuous Gap Analysis**: Comparing Current against Target identifies exact resource allocation priorities and engineering tasks.

### B. Implementation Tiers
Characterizes the maturity and formal rigor of risk governance:
1. **Tier 1 (Partial)**: Informal, ad-hoc, reactive risk management; limited organizational awareness.
2. **Tier 2 (Risk-Informed)**: Management approves risk practices, but policies are inconsistently formalized across departments.
3. **Tier 3 (Repeatable)**: Organization-wide policies are formally documented, consistently implemented, and periodically reviewed.
4. **Tier 4 (Adaptive)**: Continuous automated adaptation driven by real-time predictive threat intelligence and automated incident response runbooks.
