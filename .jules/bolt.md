## 2025-02-18 - [Root Layout Optimization]
**Learning:** The root layout (`apps/web/app/layout.tsx`) was marked with `"use client"` despite having no interactive hooks or state. This caused the entire application shell to be included in the client-side JavaScript bundle unnecessarily.
**Action:** Audit all `layout.tsx` files for unnecessary `"use client"` directives. Prioritize keeping layouts as Server Components to reduce bundle size and improve First Contentful Paint.

## 2025-02-18 - [useEffect Dependencies & State Persistence in Next.js]
**Learning:** When using `useSearchParams` in Next.js 13+ App Router, changing query parameters (e.g. via `router.replace`) triggers a re-render but may preserve component state if the component tree structure remains identical. This can lead to stale state blocking new actions if guard clauses rely on that state without checking the new parameters.
**Action:** Always validate that the current state matches the current intent (e.g. `scriptResponse.topic === topic`) before skipping an action in `useEffect`, especially when adding state variables to the dependency array.
