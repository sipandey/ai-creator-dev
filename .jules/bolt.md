## 2025-02-18 - [Root Layout Optimization]
**Learning:** The root layout (`apps/web/app/layout.tsx`) was marked with `"use client"` despite having no interactive hooks or state. This caused the entire application shell to be included in the client-side JavaScript bundle unnecessarily.
**Action:** Audit all `layout.tsx` files for unnecessary `"use client"` directives. Prioritize keeping layouts as Server Components to reduce bundle size and improve First Contentful Paint.

## 2025-02-18 - [Server Component Props Serialization]
**Learning:** Passing functional components (like Lucide icons) as props from a Server Component to a Client Component causes serialization errors because functions cannot cross the network boundary.
**Action:** When converting components to Server Components, ensure they do not pass functions/components as props. Refactor to pass them as `children` or named slots (which are passed as rendered elements, not functions).
