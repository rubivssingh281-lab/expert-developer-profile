---
name: cybersecurity-appsec
description: >-
  Use this skill when reviewing code for security vulnerabilities, conducting threat modeling, implementing authentication/authorization (OAuth2, OIDC, JWT, RBAC), mitigating OWASP Top 10 risks, hardening APIs, handling cryptographic operations, complying with NIST CSF 2.0, or defending against PortSwigger Web Security attack vectors.
---

# Cybersecurity & Application Security (AppSec) Skill

Authoritative security knowledge base, threat modeling protocols, and defensive checklists synthesizing standards from:
- **NIST Cybersecurity Framework (CSF) 2.0** — [NIST CSF 2.0 Implementation Guide](./references/nist-csf-2-implementation.md)
- **OWASP Top 10 Web Application Security Risks & Cheat Sheets** — [OWASP Cheat Sheets Engineering Compendium](./references/owasp-cheat-sheets-guide.md)
- **PortSwigger Web Security Academy Threat Vectors** — [PortSwigger Attack Playbook & Defenses](./references/portswigger-attack-playbook.md)

---

## 1. NIST Cybersecurity Framework (CSF) 2.0 Alignment

When architecting or securing systems, structure defenses across the six core functions:
1. **Govern (GV)**: Establish clear security policies, supply chain risk management, and regulatory compliance.
2. **Identify (ID)**: Maintain complete asset inventories, map data flows, identify software dependencies (SBOM), and perform continuous threat modeling.
3. **Protect (PR)**: Enforce identity management, least privilege, zero trust network architecture, data encryption in transit and at rest, and secure development lifecycles (SDLC).
4. **Detect (DE)**: Implement anomaly detection, centralized audit logging, intrusion detection, and continuous automated vulnerability scans.
5. **Respond (RS)**: Formulate automated incident response runbooks, containment protocols, and blast-radius mitigations.
6. **Recover (RC)**: Ensure verified immutable backups, disaster recovery drills, and post-incident forensic reviews.

---

## 2. OWASP Top 10 Mitigations & Cheat Sheet Standards

### A01: Broken Access Control & IDOR / BOLA
- **Principle of Least Privilege**: Verify authorization on *every single request* using cryptographic session state or token context, never relying on client-supplied IDs alone.
```python
# Vulnerable to Broken Object Level Authorization (BOLA/IDOR)
@app.get("/api/documents/{doc_id}")
async def get_doc(doc_id: UUID, db: AsyncSession = Depends(get_db)):
    return await db.get(Document, doc_id)

# Secure: Enforces Tenant/Owner Authorization Boundary
@app.get("/api/documents/{doc_id}")
async def get_doc_secure(
    doc_id: UUID,
    current_user: User = Depends(get_authenticated_user),
    db: AsyncSession = Depends(get_db),
):
    doc = await db.scalar(
        select(Document).where(
            Document.id == doc_id,
            Document.tenant_id == current_user.tenant_id  # Enforce boundary
        )
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Resource not found")
    return doc
```

### A02: Cryptographic Failures
- **Password Hashing**: Use **Argon2id** (memory: 64MB, iterations: 3, parallelism: 4) or bcrypt (cost >= 12).
- **Data Encryption**:
  - In Transit: TLS 1.3 preferred (TLS 1.2 minimum), enforce HSTS (`Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`).
  - At Rest: Authenticated encryption (**AES-256-GCM** or **ChaCha20-Poly1305**). Reject ECB or unauthenticated CBC modes.
- **Timing Safe Comparisons**: Prevent side-channel timing attacks on API tokens or hashes using `hmac.compare_digest(token_a, token_b)`.

### A03: Injection (SQL, NoSQL, OS Command, Template Injection)
- **Parameterized SQL**: Always bind variables via ORM or prepared statements. Never use f-strings or string concatenation in queries.
- **Command Injection**: Prohibit `shell=True` and `os.system()`. Always pass argument lists:
```python
# Safe invocation without shell expansion
subprocess.run(["ffmpeg", "-i", input_path, "-codec:v", "libx264", output_path], check=True)
```

### A07: Identification and Authentication Failures
- **JWT Architecture**:
  - Prefer asymmetric signing (`RS256`, `ES256`, `EdDSA`) using rotated JWKS endpoints.
  - Reject `alg: "none"` and enforce strict issuer (`iss`) and audience (`aud`) verification.
  - Storage: Store tokens in `HttpOnly`, `Secure`, `SameSite=Strict` cookies or transient memory. Never store JWTs in `localStorage`.
- **Brute-Force & Rate Limiting**: Enforce IP + account-keyed rate limits (sliding window via Redis) on authentication endpoints.

### A10: Server-Side Request Forgery (SSRF)
- Restrict outbound HTTP requests triggered by user inputs:
  - Validate and resolve URLs before fetching.
  - Reject loopback (`127.0.0.0/8`), RFC 1918 private IP spaces (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), link-local addresses, and cloud instance metadata services (`169.254.169.254`).
  - Disable HTTP redirect following on internal web hooks.

---

## 3. PortSwigger Web Security Academy Vector Mitigations

1. **CORS Misconfiguration**:
   - Never reflect the incoming `Origin` header dynamically without strict whitelist matching.
   - Never allow `null` origin.
   - Do not combine `Access-Control-Allow-Origin: *` with `Access-Control-Allow-Credentials: true`.
2. **Race Conditions & Limit Overrun**:
   - Protect concurrent operations (e.g., wallet withdrawals, coupon redemptions) with database row-level locking (`SELECT FOR UPDATE`), distributed locks (Redis Redlock), or atomic CAS (Compare-And-Swap) operations.
3. **Cross-Site Scripting (XSS)**:
   - Enforce Contextual Output Encoding for untrusted content.
   - Deploy strict Content Security Policy (CSP):
     `Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-RANDOM'; object-src 'none';`
4. **Cross-Site Request Forgery (CSRF)**:
   - Enforce `SameSite=Strict` or `Lax` cookies.
   - Use double-submit cookie patterns or anti-CSRF synchronizer tokens on state-modifying requests (`POST`, `PUT`, `DELETE`).

---

## 4. Threat Modeling Protocol (STRIDE)
When designing features or reviewing pull requests, assess against STRIDE:
- **S**poofing: Can an attacker impersonate another user or machine identity?
- **T**ampering: Can payload data or parameters in transit or storage be modified?
- **R**epudiation: Can a user deny an action without adequate audit logging?
- **I**nformation Disclosure: Are PII, secrets, or internal stack traces exposed?
- **D**enial of Service: Can an unauthenticated request exhaust memory, CPU, or DB pools?
- **E**levation of Privilege: Can an unprivileged user access administrative capabilities?
