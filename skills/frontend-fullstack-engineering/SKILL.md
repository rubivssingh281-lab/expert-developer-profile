---
name: frontend-fullstack-engineering
description: >-
  Use this skill when building modern web applications with React 19, Next.js App Router, React Server Components (RSC), Server Actions, TypeScript strict contracts, Drizzle/Prisma schemas, Tailwind CSS v4, or end-to-end Playwright testing and Core Web Vitals optimization.
trigger_patterns:
  keywords: ["react", "react 19", "nextjs", "next.js", "app router", "rsc", "server components", "server actions", "typescript", "tailwind", "playwright", "e2e", "drizzle", "frontend", "web vitals"]
  file_globs: ["**/*.tsx", "**/*.ts", "**/next.config.*", "**/playwright.config.*", "**/app/**/page.tsx", "**/actions/**"]
  architectural_intents: ["frontend-architecture", "fullstack-web-app", "rsc-boundary-design", "e2e-playwright-testing", "ui-performance-optimization"]
theta_bindings:
  governing_parameters: ["sigma", "rho", "delta"]
  parameter_mappings:
    sigma:
      local-edge: "Single Next.js Node/Bun server, SQLite/local Postgres, zero CDN edge caching complexity"
      startup-1k-rps: "Next.js App Router with ISR/Tag revalidation, Edge middleware auth check, Drizzle connection pooling"
      growth-10k-rps: "PPR (Partial Prerendering), CDN edge caching, Redis rate-limited Server Actions, distributed OpenTelemetry browser tracing"
      hyperscale-100k-rps: "Multi-region edge streaming SSR, strict bundle budgets, automated Playwright synthetic monitors across regions"
cross_skill_hooks:
  upstream:
    - skill: "fastapi-backend-architecture"
      contract: "Consumes OpenAPI / typed REST or SSE streaming endpoints with strict Zod schema validation"
  downstream:
    - skill: "cybersecurity-appsec"
      contract: "Enforces CSP headers, CSRF origin checks on Server Actions, session cookie HttpOnly/SameSite, and input sanitization"
    - skill: "devops-engineering"
      contract: "Packages standalone Next.js output in multi-stage rootless Docker containers with Playwright CI gates"
lazy_references:
  - file: "references/react19-nextjs-app-router.md"
    condition: "Activated when structuring Next.js App Router directories, RSC vs Client Component boundaries, Server Actions, or React Compiler patterns"
  - file: "references/playwright-e2e-and-web-vitals.md"
    condition: "Activated when authoring Playwright E2E test suites, auth fixtures, or optimizing Core Web Vitals (LCP, INP, CLS)"
---

# Modern Frontend & Full-Stack Web Engineering Skill

Authoritative knowledge base and production patterns synthesizing modern web standards from:
- **React 19 & Next.js App Router Architecture** — [React 19 & Next.js App Router Reference](./references/react19-nextjs-app-router.md)
- **Resilient E2E Testing & Web Performance** — [Playwright E2E & Core Web Vitals Reference](./references/playwright-e2e-and-web-vitals.md)

---

## 1. React 19 & Server-First Architecture

1. **Compiler-First Optimization**: With the React 19 Compiler enabled, manual `useMemo`, `useCallback`, and `React.memo` wrappers are obsolete. Write clean, declarative components and let the compiler memoize at the AST level.
2. **Server Components by Default**: Fetch database records, validate secrets, and render heavy dependencies (Markdown parsers, syntax highlighters) inside React Server Components (RSC). Push `"use client"` strictly to interactive **leaf components**.
3. **End-to-End Type Safety**: Share types directly from the database schema (Drizzle / Prisma) and Zod validation schemas through Server Actions down to React form hooks (`useActionState`, `useOptimistic`).

---

## 2. Security at the Server Action Boundary

Every Next.js Server Action is a public HTTP `POST` endpoint under the hood:
- Never trust arguments passed to a Server Action.
- Always re-verify user authentication (`session.userId`) and object ownership (BOLA/IDOR) inside every Server Action.
- Parse inputs strictly with `zod.safeParse()` before mutating state, then call `revalidatePath()` or `revalidateTag()`.
