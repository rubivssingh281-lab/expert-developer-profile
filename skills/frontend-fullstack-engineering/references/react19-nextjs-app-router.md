# React 19, Next.js App Router & Type-Safe Full-Stack Architecture

Authoritative manual for structuring React 19 and Next.js App Router applications with Server Components, validated Server Actions, and zero-boilerplate full-stack type safety.

---

## 1. Scalable App Router Directory Layout

```text
app/
├── (auth)/                  # Route group for unauthenticated flows
│   ├── login/page.tsx
│   └── register/page.tsx
├── dashboard/
│   ├── error.tsx            # Route-level error boundary
│   ├── loading.tsx          # Streaming Suspense fallback
│   ├── page.tsx             # Server Component (direct DB/API reads)
│   └── _components/         # Route-private Client leaf components
│       └── create-post-form.tsx
├── layout.tsx               # Root shell (fonts, metadata, providers)
actions/
└── post.actions.ts          # Validated Server Actions (mutations)
db/
├── schema.ts                # Drizzle / SQLAlchemy-mirrored schema
└── client.ts
```

---

## 2. Server Component Data Fetching & Client Leaves

Avoid creating internal REST endpoints solely for your own Server Components to `fetch()`. Query databases or internal backend services directly on the server and pass serialized props down to interactive Client leaves:

```tsx
// app/dashboard/page.tsx (Server Component)
import { db } from "@/db/client";
import { postsTable } from "@/db/schema";
import { eq } from "drizzle-orm";
import { requireSession } from "@/lib/auth";
import { CreatePostForm } from "./_components/create-post-form";

export default async function DashboardPage() {
  const session = await requireSession();
  const posts = await db
    .select()
    .from(postsTable)
    .where(eq(postsTable.ownerId, session.userId));

  return (
    <main className="mx-auto max-w-4xl p-6 space-y-6">
      <h1 className="text-2xl font-semibold">Workspace Posts</h1>
      <CreatePostForm />
      <ul className="space-y-2">
        {posts.map((p) => (
          <li key={p.id} className="rounded border p-3">{p.title}</li>
        ))}
      </ul>
    </main>
  );
}
```

---

## 3. Validated Server Actions with `useActionState`

Every Server Action must enforce authentication, Zod input validation, and authorization before mutating state:

```typescript
// actions/post.actions.ts
"use server";

import { z } from "zod";
import { revalidatePath } from "next/cache";
import { db } from "@/db/client";
import { postsTable } from "@/db/schema";
import { requireSession } from "@/lib/auth";

const CreatePostSchema = z.object({
  title: z.string().trim().min(3).max(120),
});

export type ActionResult = { error?: string; ok?: boolean } | null;

export async function createPost(_prev: ActionResult, formData: FormData): Promise<ActionResult> {
  const session = await requireSession();
  const parsed = CreatePostSchema.safeParse({ title: formData.get("title") });
  if (!parsed.success) {
    return { error: parsed.error.issues[0]?.message ?? "Invalid input" };
  }

  await db.insert(postsTable).values({
    title: parsed.data.title,
    ownerId: session.userId,
  });

  revalidatePath("/dashboard");
  return { ok: true };
}
```

Client leaf binding using React 19 `useActionState`:

```tsx
// app/dashboard/_components/create-post-form.tsx
"use client";

import { useActionState } from "react";
import { createPost } from "@/actions/post.actions";

export function CreatePostForm() {
  const [state, formAction, isPending] = useActionState(createPost, null);

  return (
    <form action={formAction} className="flex gap-3">
      <input name="title" required placeholder="New post title" className="border rounded px-3 py-2 flex-1" />
      <button type="submit" disabled={isPending} className="bg-black text-white px-4 py-2 rounded">
        {isPending ? "Saving..." : "Create"}
      </button>
      {state?.error && <p role="alert" className="text-sm text-red-600">{state.error}</p>}
    </form>
  );
}
```
