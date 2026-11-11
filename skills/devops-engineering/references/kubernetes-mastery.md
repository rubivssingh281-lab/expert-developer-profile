# Kubernetes Architecture & Production Mastery Reference

Synthesized from **Kubernetes Official Documentation, Concepts & Gateway API**.

---

## 1. Workload Controllers & Stateful Sets
- **Deployments**: Standard for stateless microservices. Enforce `RollingUpdate` with `maxSurge: 25%` and `maxUnavailable: 0` for zero-downtime deployments.
- **StatefulSets**: For distributed consensus engines (Kafka, ZooKeeper, Elasticsearch, PostgreSQL primaries). Provides stable network identities (`pod-0.service.ns.svc.cluster.local`) and ordered automated rolling updates.
- **DaemonSets**: For node-level agents (Log forwarders, OpenTelemetry collectors, Cilium/Calico CNI pods).
- **Jobs & CronJobs**: Ephemeral tasks. Configure `backoffLimit`, `activeDeadlineSeconds`, and `concurrencyPolicy: Forbid`.

---

## 2. Pod Lifecycle & Three-Probe Architecture
A resilient Kubernetes pod must configure all three probes correctly:

| Probe | Purpose | Failure Consequence | Period / Threshold |
| :--- | :--- | :--- | :--- |
| **`startupProbe`** | Handles slow initializations (ORM warmups, ML model loading). | Disables liveness/readiness checks until passing; kills container if `failureThreshold * periodSeconds` expires. | `periodSeconds: 2-5`, `failureThreshold: 30` |
| **`livenessProbe`** | Detects deadlocks or unrecoverable freezes. | Kills and restarts the container. | `periodSeconds: 15-30`, `timeoutSeconds: 3` |
| **`readinessProbe`** | Detects temporary unreadiness (DB reconnection, queue backpressure). | Removes Pod IP from Service Endpoints; **does NOT restart** container. | `periodSeconds: 5-10`, `timeoutSeconds: 2` |

### PreStop Hook & Graceful Draining
```yaml
lifecycle:
  preStop:
    exec:
      # Sleep gives kube-proxy time to remove pod from endpoints before SIGTERM
      command: ["/bin/sh", "-c", "sleep 5"]
```
*Why sleep 5?* Kubernetes endpoint updates propagate asynchronously to `kube-proxy` across all nodes. Without a small sleep in `preStop`, incoming requests might still be routed to a pod that has already received `SIGTERM`.

---

## 3. Resource Management & Quality of Service (QoS)
Kubernetes assigns each Pod a QoS class based on requests and limits:

1. **Guaranteed (Highest Priority)**:
   - Every container has `requests.cpu == limits.cpu` AND `requests.memory == limits.memory`.
   - Never evicted during node memory pressure unless exhausting its own memory limit.
   - Ideal for production APIs, payment services, databases.
2. **Burstable**:
   - `requests` are defined, but `limits > requests`.
   - Evicted when the node is under severe pressure after BestEffort pods are terminated.
3. **BestEffort (Lowest Priority)**:
   - Neither requests nor limits are declared.
   - First to be OOMKilled when node resources run low. Never use in production.

---

## 4. Network Policies (Zero Trust Cluster Networking)
By default, all pods in a Kubernetes cluster can communicate with all other pods. Enforce default-deny NetworkPolicies:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-api-to-db
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend-api
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: postgres-db
      ports:
        - protocol: TCP
          port: 5432
```

---

## 5. Kubernetes Gateway API Standard (`gateway.networking.k8s.io`)
The Kubernetes Gateway API is the official next-generation standard succeeding legacy `Ingress`. It decouples infrastructure provisioning from application routing through a role-oriented architecture:

```text
               ┌─────────────────────────────────┐
               │    GatewayClass (Infra Team)    │ (e.g. Envoy, Istio, Cilium)
               └────────────────┬────────────────┘
                                │
               ┌────────────────▼────────────────┐
               │     Gateway (Cluster Ops)       │ (IP, Ports, TLS termination)
               └────────────────┬────────────────┘
                                │
         ┌──────────────────────┴──────────────────────┐
         ▼                                             ▼
┌─────────────────────────┐               ┌─────────────────────────┐
│ HTTPRoute: API Service  │               │ HTTPRoute: ML Inference │ (App Devs)
└───────────┬─────────────┘               └───────────┬─────────────┘
            ▼                                         ▼
┌─────────────────────────┐               ┌─────────────────────────┐
│ Service: backend-api    │               │ Service: ml-serving     │
└─────────────────────────┘               └─────────────────────────┘
```

### Production Gateway API Blueprint
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: platform-gateway
  namespace: production
spec:
  gatewayClassName: envoy-gateway
  listeners:
    - name: https
      protocol: HTTPS
      port: 443
      tls:
        mode: Terminate
        certificateRefs:
          - name: platform-wildcard-tls
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: api-routing
  namespace: production
spec:
  parentRefs:
    - name: platform-gateway
  hostnames:
    - "api.platform.internal"
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /api/v1/predict
      # Weighted Canary Shifting (90% stable, 10% canary)
      backendRefs:
        - name: api-inference-service
          port: 8000
          weight: 90
        - name: api-inference-service-canary
          port: 8000
          weight: 10
      filters:
        - type: RequestHeaderModifier
          requestHeaderModifier:
            add:
              - name: X-Gateway-Routed
                value: "true"
```
