## 2025-02-18 - [Root Layout Optimization]
**Learning:** The root layout (`apps/web/app/layout.tsx`) was marked with `"use client"` despite having no interactive hooks or state. This caused the entire application shell to be included in the client-side JavaScript bundle unnecessarily.
**Action:** Audit all `layout.tsx` files for unnecessary `"use client"` directives. Prioritize keeping layouts as Server Components to reduce bundle size and improve First Contentful Paint.

## 2025-02-18 - [Date Hydration Mismatch & Prefetching]
**Learning:** Rendering date-dependent UI (e.g., highlighting "Today") in a component without ensuring client/server consistency causes hydration errors. Using `new Date()` directly in a Server Component (or even a Client Component during SSR) captures the server's time, which may differ from the user's.
**Action:** Calculate time-sensitive values in a top-level Client Component (or using a `useClientOnly` hook) and pass them as props to presentational components. When optimizing lists, replace `useRouter().push()` with `<Link>` to enable automatic prefetching and reduce JS execution.
