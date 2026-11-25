# Playwright E2E Testing & Core Web Vitals Optimization

Authoritative guide for building deterministic, non-flaky Playwright E2E suites against live servers and optimizing Core Web Vitals (`LCP`, `INP`, `CLS`).

---

## 1. Production Playwright Configuration

Always test against a real server and live test database rather than fragile mocked API responses. Enable trace capture on first retry for instant post-mortem debugging in CI:

```typescript
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 2 : undefined,
  reporter: [["html", { open: "never" }], ["github"]],
  use: {
    baseURL: "http://127.0.0.1:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  projects: [
    { name: "setup", testMatch: /.*\.setup\.ts/ },
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"], storageState: "playwright/.auth/user.json" },
      dependencies: ["setup"],
    },
  ],
  webServer: {
    command: "npm run start",
    url: "http://127.0.0.1:3000",
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
});
```

---

## 2. Accessible Locators & Deterministic Assertions

Avoid brittle CSS or XPath selectors. Query the DOM using user-facing accessibility roles (`getByRole`, `getByLabel`, `getByText`) so tests simultaneously validate ARIA accessibility:

```typescript
// tests/e2e/dashboard.spec.ts
import { test, expect } from "@playwright/test";

test("creates a post and survives reload", async ({ page }) => {
  await page.goto("/dashboard");
  await page.getByPlaceholder("New post title").fill("Production RSC Guide");
  await page.getByRole("button", { name: /create/i }).click();

  await expect(page.getByText("Production RSC Guide")).toBeVisible();
  await page.reload();
  await expect(page.getByText("Production RSC Guide")).toBeVisible();
});
```

---

## 3. Core Web Vitals Hardening Budgets

| Metric | Target | Production Enforcement |
| :--- | :--- | :--- |
| **LCP** (Largest Contentful Paint) | `< 2.5s` | Server-render above-the-fold content via RSC; preload hero images with `priority` (`next/image`). |
| **INP** (Interaction to Next Paint) | `< 200ms` | Offload heavy transforms off main thread; leverage `useTransition` / `useActionState` to yield frames. |
| **CLS** (Cumulative Layout Shift) | `< 0.1` | Always reserve explicit `width`/`height` or aspect-ratio boxes; use `next/font` zero-shift font loading. |
