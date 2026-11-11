# OWASP Cheat Sheet Series Engineering Compendium

Synthesized from the **OWASP Cheat Sheet Series (Defensive Implementation Guidelines)**.

---

## 1. Password Storage Cheat Sheet Standard
- **Recommended Algorithm**: **Argon2id** (OWASP preferred primary algorithm).
  - Memory Cost: $m \ge 65536 \text{ KiB}$ ($64 \text{ MiB}$)
  - Time Cost: $t \ge 3 \text{ iterations}$
  - Parallelism: $p \ge 4 \text{ threads}$
  - Salt: Cryptographically random 16 bytes minimum generated via CSPRNG (`os.urandom(16)`).
- **Secondary Algorithm**: **Bcrypt** with work factor (cost) $\ge 12$.
- **Prohibited**: MD5, SHA-1, raw SHA-256/SHA-512 (vulnerable to high-throughput GPU/ASIC rainbow attacks).

---

## 2. Cross-Site Scripting (XSS) Prevention Cheat Sheet
1. **Context-Aware Encoding**:
   - HTML Body: `& -> &amp;`, `< -> &lt;`, `> -> &gt;`, `" -> &quot;`, `' -> &#x27;`.
   - JavaScript Variables: Encode using JSON serialization (`json.dumps()`) rather than direct template string formatting.
2. **Content Security Policy (CSP)**:
   ```http
   Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-rAnd0m123'; object-src 'none'; base-uri 'none'; require-trusted-types-for 'script';
   ```
3. **Cookie Flags**:
   Always set `HttpOnly` on sensitive session/auth cookies to prevent client-side JavaScript access via `document.cookie`.

---

## 3. Cross-Site Request Forgery (CSRF) Prevention Cheat Sheet
- **SameSite Cookies**:
  - `SameSite=Strict`: Cookie is never sent on cross-site requests.
  - `SameSite=Lax`: Cookie sent only on top-level safe GET navigations. Standard baseline.
- **Synchronizer Token Pattern**:
  - Cryptographically random anti-CSRF token bound to the user session.
  - Required in HTTP headers (`X-CSRF-Token`) for all state-changing requests (`POST`, `PUT`, `DELETE`, `PATCH`).

---

## 4. Server-Side Request Forgery (SSRF) Prevention Cheat Sheet
When an application must fetch a remote URL provided by a user:
1. **URL Parsing & Validation**: Parse protocol (strictly permit `https://`, ban `file://`, `gopher://`, `dict://`).
2. **DNS Resolution Verification**:
   - Resolve hostname to IP address *before* sending request.
   - Block private and internal IP ranges:
     - `127.0.0.0/8` (Loopback)
     - `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` (RFC 1918)
     - `169.254.169.254` (Cloud metadata endpoint for AWS, GCP, Azure)
     - `::1` (IPv6 loopback), `fe80::/10` (IPv6 link-local)
3. **Disable Redirects**: Prevent attackers from bypassing checks via HTTP 301/302 redirects to internal IP addresses.

---

## 5. REST & Microservices Security Cheat Sheets
- **HTTP Methods**: Strictly enforce semantics: `GET` must be safe and idempotent (no state mutation).
- **Security Headers**:
  ```http
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), camera=(), microphone=()
  ```
- **Microservices Identity Propagation**:
  - Pass authenticated caller identity across internal service hops using cryptographically signed, short-lived internal JWTs (Service-to-Service tokens).
  - Enforce mutual TLS (mTLS) for all inter-service mesh communications.
- **Session ID Entropy & Rotation**:
  - Session IDs must possess $\ge 128 \text{ bits}$ of entropy from a CSPRNG.
  - **Session Rotation**: Invalidate existing session ID and issue a new session token immediately upon any privilege level change (e.g. login, 2FA completion, password change) to neutralize session fixation attacks.
- **Mishandling of Exceptional Conditions (OWASP 2025 A10)**:
  - Catch unhandled exceptions at framework boundaries.
  - Return standardized RFC 7807 problem payloads without leaking stack traces, memory addresses, or database connection strings.
