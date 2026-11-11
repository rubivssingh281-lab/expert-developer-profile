# Docker BuildKit Production Reference

Synthesized from **Docker Official Building Best Practices** and modern container engineering standards.

---

## 1. BuildKit Advanced Cache Mounts
Rebuilding dependencies from scratch in containers is operational toil. BuildKit provides dedicated cache mounts (`--mount=type=cache`) that persist package manager caches between runs without polluting the resulting image layer:

### Pip (Python)
```dockerfile
# syntax=docker/dockerfile:1.7
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user -r requirements.txt
```

### APT (Debian/Ubuntu)
```dockerfile
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl
```

### NPM / Yarn / Pnpm (Node.js)
```dockerfile
RUN --mount=type=cache,target=/root/.npm \
    npm ci --prefer-offline
```

### Cargo (Rust)
```dockerfile
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release
```

---

## 2. Secrets & SSH Mounts at Build Time
Never use `ARG` or `ENV` to pass private keys, tokens, or credentials into builds—they get baked into image layers. Use BuildKit secret mounts:

```dockerfile
# Mounting credentials safely without leaking into image layers
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm install

RUN --mount=type=ssh \
    git clone git@github.com:private-org/private-repo.git
```
Build command:
```bash
docker build --secret id=npmrc,src=.npmrc --ssh default -t my-app .
```

---

## 3. Layer Invalidation & Instruction Ordering Rules
Docker builds execute top-to-bottom. A change on line $N$ invalidates the cache for all subsequent lines $N+1 \dots M$:

1. **System packages & OS dependencies**: Rarely change. Place first.
2. **Language manifest files (`requirements.txt`, `package.json`, `Cargo.toml`)**: Change occasionally.
3. **Dependency installation step**: Cached unless manifest changes.
4. **Application source code**: Changes on every commit. Place last.

---

## 4. Rootless Execution & Security Context
- **Never run as UID 0**: Create an unprivileged user (`groupadd -g 10001 appgroup && useradd -u 10001 -g appgroup appuser`).
- **Read-Only Root Filesystem**: Configure runtime to run with `--read-only`. Mount writeable temporary directories as `tmpfs` (`/tmp`).
- **Drop Linux Capabilities**: Drop `ALL` and add only what is explicitly needed (e.g., `NET_BIND_SERVICE`).
