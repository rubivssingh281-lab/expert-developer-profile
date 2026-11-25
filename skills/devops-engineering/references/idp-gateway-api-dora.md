# Internal Developer Platforms (IDPs), Kubernetes Gateway API & DORA Craftsmanship

Authoritative manual for modern Platform Engineering paved roads, migrating from legacy Ingress to Kubernetes Gateway API, Trunk-Based Development, and DORA reliability metrics.

---

## 1. Internal Developer Platforms (IDPs) for Humans & AI Agents

Platform Engineering eliminates cognitive load by providing self-service **Golden Paths (Paved Roads)**:
- **Standardized Service Templates**: Developers and autonomous AI agents scaffold new services via approved blueprints (FastAPI + Docker BuildKit + OTel + Cilium policies) rather than hand-crafting insecure YAML.
- **Agent-Safe Platform Consumers**: Treat AI coding and ops agents as first-class IDP consumers by exposing sandboxed, RBAC-scoped APIs, ephemeral preview environments, and deterministic CI gates—preventing *"phantom velocity"* (shipping faster only to multiply production incidents).

---

## 2. Kubernetes Gateway API (Replacing Legacy Ingress)

The **Kubernetes Gateway API** replaces annotation-overloaded `Ingress` objects with role-oriented, portable CRDs (`GatewayClass`, `Gateway`, `HTTPRoute`) supporting native traffic splitting, header matching, and zero-downtime canary rollouts:

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: api-canary-route
  namespace: production
spec:
  parentRefs:
    - name: prod-gateway
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /v1/inference
      backendRefs:
        - name: fastapi-pytorch-stable
          port: 8000
          weight: 90
        - name: fastapi-pytorch-canary
          port: 8000
          weight: 10
```

---

## 3. Small-Batch Trunk-Based Delivery & DORA Metrics

| DORA Metric | Elite Target | Engineering Enforcement |
| :--- | :--- | :--- |
| **Deployment Frequency** | Multiple per day | Small-batch trunk-based PRs (`< 400` LOC) merged behind feature flags. |
| **Lead Time for Changes** | `< 1 hour` | Shift-Left test pyramid keeping local + CI feedback loops under 10 minutes. |
| **Change Failure Rate (CFR)** | `< 5%` | Automated SAST (`bandit`, `ruff`), contract tests, and canary burn-rate rollbacks. |
| **Mean Time to Recovery (MTTR)** | `< 1 hour` | Unified OpenTelemetry traces + automated `Gateway` traffic shift rollback. |
