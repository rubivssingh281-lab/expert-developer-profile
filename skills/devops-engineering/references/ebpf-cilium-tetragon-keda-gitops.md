# eBPF Kernel Enforcement (Cilium + Tetragon), KEDA GPU Scaling & Google SRE Multi-Burn Rate Alerting

Authoritative engineering manual on eBPF runtime container security, event-driven KEDA GPU autoscaling, and Google SRE multi-window multi-burn-rate alerting.

---

## 1. eBPF Kernel-Level Enforcement (Cilium + Tetragon)

### 1.1 Cilium Network Policy (L7 HTTP & DNS Allowlisting)
Enforces zero-trust egress and ingress at the Linux kernel eBPF layer:

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: fastapi-pytorch-policy
  namespace: production
spec:
  endpointSelector:
    matchLabels:
      app: fastapi-pytorch-service
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: ingress-gateway
      toPorts:
        - ports:
            - port: "8000"
              protocol: TCP
          rules:
            http:
              - method: "GET"
                path: "/health/.*"
              - method: "POST"
                path: "/v1/inference"
  egress:
    - toEndpoints:
        - matchLabels:
            app: postgresql
      toPorts:
        - ports:
            - port: "5432"
              protocol: TCP
```

### 1.2 Tetragon TracingPolicy (Process & Binary Execution Lockout)
Blocks execution of unauthorized shells or network binaries (`/bin/sh`, `curl`, `wget`) inside production containers:

```yaml
apiVersion: cilium.io/v1alpha1
kind: TracingPolicy
metadata:
  name: block-shell-execution
  namespace: production
spec:
  kprobes:
    - call: "sys_execve"
      syscall: true
      args:
        - index: 0
          type: "string"
      selectors:
        - matchArgs:
            - index: 0
              operator: "In"
              values:
                - "/bin/sh"
                - "/bin/bash"
                - "/usr/bin/curl"
                - "/usr/bin/wget"
          matchActions:
            - action: Sigkill
```

---

## 2. KEDA GPU Inference Auto-Scaling

Scales GPU worker pods based on real-time Prometheus queue metrics from vLLM:

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: vllm-gpu-scaler
  namespace: production
spec:
  scaleTargetRef:
    name: vllm-inference-worker
  minReplicaCount: 1
  maxReplicaCount: 8
  cooldownPeriod: 300
  advanced:
    horizontalPodAutoscalerConfig:
      behavior:
        scaleDown:
          stabilizationWindowSeconds: 300
  triggers:
    - type: prometheus
      metadata:
        serverAddress: http://prometheus-k8s.monitoring.svc:9090
        metricName: vllm_num_requests_waiting
        query: sum(vllm:num_requests_waiting{namespace="production"})
        threshold: "4"
```

---

## 3. Google SRE Multi-Window Multi-Burn-Rate Alerts

| Alert Class | Time Window | Burn Rate | Error Budget Consumed | Severity | Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **P1 Page** | 1 Hour | 14.4x | 2.0% | Critical | Automated Rollback + On-Call Page |
| **P1 Page** | 6 Hours | 6.0x | 5.0% | High | On-Call Page |
| **P2 Ticket** | 3 Days | 1.0x | 10.0% | Medium | SRE Incident Ticket |
