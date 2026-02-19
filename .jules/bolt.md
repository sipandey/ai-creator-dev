## 2025-02-18 - [Root Layout Optimization]
**Learning:** The root layout (`apps/web/app/layout.tsx`) was marked with `"use client"` despite having no interactive hooks or state. This caused the entire application shell to be included in the client-side JavaScript bundle unnecessarily.
**Action:** Audit all `layout.tsx` files for unnecessary `"use client"` directives. Prioritize keeping layouts as Server Components to reduce bundle size and improve First Contentful Paint.

## 2025-02-18 - [Next.js Client Component Double Fetch]
**Learning:** In Next.js client components using `useSearchParams`, updating the URL (e.g., via `router.replace`) triggers a re-render and re-runs `useEffect`. If the effect fetches data based on params, and the initial action (like a form submission) already fetched that data and updated the state *before* the URL change, a redundant fetch occurs.
**Action:** Always implement a "check-then-fetch" pattern in `useEffect`: verify if the current local state already matches the new URL parameters (e.g., `if (data?.id === currentId) return;`) before initiating a new network request.
