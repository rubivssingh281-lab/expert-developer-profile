---
name: devops-engineering
description: >-
  Use this skill when designing, building, automating, or troubleshooting DevOps workflows, CI/CD pipelines (GitHub Actions, GitLab CI), Docker BuildKit containers, Kubernetes architecture, Helm charts, HashiCorp Terraform (IaC), Linux administration, and Google SRE observability practices.
---

# DevOps, Cloud Infrastructure & SRE Engineering Skill

Authoritative knowledge base and operational runbooks synthesizing standards from:
- **Kubernetes Official Concepts & Architecture** — [Kubernetes Architecture Mastery Reference](./references/kubernetes-mastery.md)
- **Docker Official Building Best Practices & BuildKit** — [Docker BuildKit Production Reference](./references/docker-buildkit-production.md)
- **Google Site Reliability Engineering (SRE) Book** — [Google SRE Handbook & Math](./references/google-sre-handbook.md)
- **HashiCorp Terraform Documentation & Architecture** — [Terraform Enterprise Architecture Reference](./references/terraform-enterprise.md)

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

## 3. Google Site Reliability Engineering (SRE) Doctrine

### Core Principles
1. **Service Level Indicators (SLIs)**: Quantifiable metrics representing service health (e.g., HTTP 5xx error rate, p99 latency < 200ms).
2. **Service Level Objectives (SLOs)**: Target reliability agreed upon with stakeholders (e.g., 99.9% of requests succeed in a 30-day rolling window).
3. **Error Budget**: The remaining headroom ($100\% - \text{SLO} = 0.1\%$). When the error budget is exhausted, freeze feature deployments and focus exclusively on stability.
4. **Toil Elimination**: Any operational work that is manual, repetitive, automatable, tactical, and lacks enduring value must be capped at `< 50%` of an engineer's time; automate the remainder.
5. **Cascading Failure Defense**:
   - Implement exponential backoff with jitter on all network clients.
   - Deploy circuit breakers (fail-fast instead of queuing timeouts).
   - Implement load shedding when memory/CPU saturation exceeds safe thresholds.
6. **Blameless Post-Mortems**: Incidents are learning opportunities caused by systemic flaws, not individual incompetence. Document timeline, root causes, detection gap, and actionable remediation items.

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
