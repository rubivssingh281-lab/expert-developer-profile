---
name: devops-engineering
description: >-
  Use this skill when designing, building, automating, or troubleshooting DevOps workflows, CI/CD pipelines (GitHub Actions, GitLab CI), Docker BuildKit containers, Kubernetes architecture, Helm charts, HashiCorp Terraform (IaC), Linux administration, and Google SRE observability practices.
trigger_patterns:
  keywords: ["docker", "buildkit", "kubernetes", "k8s", "helm", "terraform", "sre", "sli", "slo", "prometheus", "grafana", "opentelemetry", "ci/cd", "github actions", "littles law", "burn rate"]
  file_globs: ["**/Dockerfile*", "**/docker-compose*.yaml", "**/*.tf", "**/*.hcl", "**/k8s/**", "**/*.yaml", "**/.github/workflows/**"]
  architectural_intents: ["container-hardening", "k8s-workload-manifests", "iac-automation", "sre-alerting-design", "capacity-planning", "ci-cd-pipeline-hardening"]
theta_bindings:
  governing_parameters: ["sigma", "delta"]
  parameter_mappings:
    sigma:
      local-edge: "Single docker-compose, local sqlite/pg, zero-k8s overhead, minimal resource requests"
      startup-1k-rps: "Kubernetes 3-replica Deployment, ingress-nginx, HPA cpu 75%, basic Prometheus alerts"
      growth-10k-rps: "Guaranteed QoS, multi-AZ topologySpreadConstraints, PodDisruptionBudget, KEDA autoscaling, multi-burn-rate alerts"
      hyperscale-100k-rps: "Multi-cluster service mesh, Gateway API, LIFO queue load shedding, PgBouncer sidecars, distributed rate-limiting"
cross_skill_hooks:
  upstream:
    - skill: "fastapi-backend-architecture"
      contract: "Provides healthz/readyz probe endpoints, lifespan graceful drain, and Prometheus metrics"
    - skill: "cybersecurity-appsec"
      contract: "Defines non-root UID 10001, drop ALL capabilities, read-only root filesystems, and sealed secrets"
  downstream:
    - skill: "aiml-engineering"
      contract: "Provisions GPU device plugins, tolerations, and resource limits for model inference pods"
lazy_references:
  - file: "references/docker-buildkit-production.md"
    condition: "Activated when crafting Dockerfile builds, multi-stage pipelines, cache mounts, or distroless packaging"
  - file: "references/kubernetes-mastery.md"
    condition: "Activated when designing Deployments, StatefulSets, 3-probe patterns, NetworkPolicies, or PDBs"
  - file: "references/google-sre-handbook.md"
    condition: "Activated when calculating SLIs/SLOs, multi-window burn rate alerts, Little's Law concurrency, or load shedding"
  - file: "references/terraform-enterprise.md"
    condition: "Activated when authoring HCL modules, remote state locking, moved blocks, or lifecycle preconditions"
  - file: "references/ebpf-cilium-tetragon-keda-gitops.md"
    condition: "Activated when deploying Cilium eBPF L7 network policies, Tetragon kernel execution guards, or KEDA GPU autoscalers"
  - file: "references/idp-gateway-api-dora.md"
    condition: "Activated when designing Internal Developer Platforms (IDPs), Kubernetes Gateway API routes, or DORA/Trunk-Based CI pipelines"
---

# DevOps, Cloud Infrastructure & SRE Engineering Skill

Authoritative knowledge base and operational runbooks synthesizing standards from:
- **Kubernetes Official Concepts & Architecture** — [Kubernetes Architecture Mastery Reference](./references/kubernetes-mastery.md)
- **Docker Official Building Best Practices & BuildKit** — [Docker BuildKit Production Reference](./references/docker-buildkit-production.md)
- **Google Site Reliability Engineering (SRE) Book** — [Google SRE Handbook & Math](./references/google-sre-handbook.md)
- **HashiCorp Terraform Documentation & Architecture** — [Terraform Enterprise Architecture Reference](./references/terraform-enterprise.md)
- **eBPF Cilium, Tetragon & KEDA GPU Scaling** — [eBPF, Tetragon & KEDA Reference](./references/ebpf-cilium-tetragon-keda-gitops.md)
- **Platform Engineering, Gateway API & DORA** — [IDP, Gateway API & DORA Reference](./references/idp-gateway-api-dora.md)

---

## 1. Docker Building Best Practices (BuildKit Standard)

### High-Performance Multi-Stage Dockerfile Blueprint
```dockerfile
# syntax=docker/dockerfile:1.7
# Stage 1: Build & Dependency Resolution
FROM python:3.12-slim-bookworm AS builder

WORKDIR /build
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Leverage BuildKit pip cache mount to accelerate rebuilds
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user -r requirements.txt

# Stage 2: Minimal Distroless/Slim Production Runtime
FROM python:3.12-slim-bookworm AS runtime

WORKDIR /app
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Non-root user with dedicated UID/GID
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/sh -m appuser

# Copy installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appgroup . /app

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=20s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/healthz || exit 1

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Build Quality Checklist
- **BuildKit Caching**: Use `--mount=type=cache` for package managers (`apt`, `pip`, `npm`, `cargo`).
- **Layer Optimization**: Order instructions from least frequently changing (system deps) to most frequently changing (app code).
- **Security Posture**: Never run as `root`; drop unnecessary Linux capabilities; omit build tools (`gcc`, `curl`) from the final runtime image.
- **Strict `.dockerignore`**: Exclude `.git`, `.env*`, `*.pyc`, `__pycache__`, `tests`, `node_modules`.

---

## 2. Kubernetes Architectural Standards

### Production Deployment Manifest Pattern
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
  labels:
    app.kubernetes.io/name: api-service
    app.kubernetes.io/part-of: backend-platform
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: api-service
  template:
    metadata:
      labels:
        app: api-service
    spec:
      terminationGracePeriodSeconds: 60
      containers:
        - name: api
          image: ghcr.io/org/api-service:v1.4.2
          imagePullPolicy: IfNotPresent
          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
            limits:
              cpu: "1000m"
              memory: "1Gi"
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            runAsNonRoot: true
            runAsUser: 10001
            capabilities:
              drop: ["ALL"]
          # Kubernetes Three-Probe Pattern
          startupProbe:
            httpGet:
              path: /readyz
              port: 8000
            failureThreshold: 30
            periodSeconds: 2
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8000
            periodSeconds: 15
            timeoutSeconds: 3
          readinessProbe:
            httpGet:
              path: /readyz
              port: 8000
            periodSeconds: 10
            timeoutSeconds: 2
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: api-service-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: api-service
```

### Key Kubernetes Concepts
1. **Pod Lifecycle & Graceful Drain**: Listen for `SIGTERM` in application code, pause traffic intake, drain in-flight requests, and flush logs before `terminationGracePeriodSeconds` expires.
2. **QoS Classes**: Ensure predictable performance by matching `requests` and `limits` for CPU/Memory to achieve **Guaranteed QoS**, preventing OOMKills under node pressure.
3. **PodDisruptionBudget (PDB)**: Enforce high availability during cluster upgrades or node draining.

---

## 3. Google Site Reliability Engineering (SRE) Doctrine & Math

### Core Principles & Mathematical Formulas
1. **Service Level Indicators (SLIs)**: Quantifiable metrics representing service health (e.g., HTTP 5xx error rate, p99 latency < 200ms).
2. **Service Level Objectives (SLOs)**: Target reliability agreed upon with stakeholders (e.g., 99.9% of requests succeed in a 30-day rolling window).
3. **Error Budget**: The remaining headroom:
   $$\text{Error Budget} = 1 - \text{SLO}_{\text{target}}$$
4. **Little's Law Concurrency Calculation**:
   $$L = \lambda \times W_{\text{P99}}$$
   Where $L$ is concurrency in flight, $\lambda$ is arrival throughput (RPS), and `W_P99` is P99 latency in seconds.
5. **Multi-Window Multi-Burn-Rate Alerting (Google SRE Standard for 99.9% SLO)**:
   - **Critical Page ($14.4\times$ burn)**: 1-hour long window AND 5-minute short window (consumes 2% budget in 1 hour).
   - **Critical Page ($6\times$ burn)**: 6-hour long window AND 30-minute short window (consumes 5% budget in 6 hours).
   - **Ticket ($1\times$ burn)**: 3-day long window AND 6-hour short window (consumes 10% budget in 3 days).
6. **Toil Elimination**: Cap manual repetitive tasks at `< 50%` of an engineer's time; automate the remainder.
7. **Cascading Failure Defense**: Deploy exponential backoff with full jitter, circuit breakers, and LIFO queue scheduling under overload.

---

## 4. HashiCorp Terraform (Infrastructure as Code)

### Production Module Blueprint
```hcl
terraform {
  required_version = ">= 1.7.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  # Remote backend with state locking
  backend "s3" {
    bucket         = "prod-terraform-state-vault"
    key            = "services/api/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

variable "environment" {
  type        = string
  description = "Deployment target environment (dev/staging/prod)"
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}
```

### Terraform Workflow & Hygiene
- **Remote State & Locking**: Always store state in a remote encrypted backend (S3+DynamoDB, GCS, or Terraform Cloud) with distributed state locking enabled.
- **Module Structure**: Separate modules into root configurations and reusable submodules (`main.tf`, `variables.tf`, `outputs.tf`).
- **Safety Lifecycle**: Use `lifecycle { prevent_destroy = true }` on stateful databases and `lifecycle { create_before_destroy = true }` on zero-downtime resource updates.
- **CI Linting**: Run `terraform fmt -check`, `terraform validate`, and `tflint` in CI before creating speculative execution plans.
