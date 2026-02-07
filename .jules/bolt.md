## 2025-02-18 - [Root Layout Optimization]
**Learning:** The root layout (`apps/web/app/layout.tsx`) was marked with `"use client"` despite having no interactive hooks or state. This caused the entire application shell to be included in the client-side JavaScript bundle unnecessarily.
**Action:** Audit all `layout.tsx` files for unnecessary `"use client"` directives. Prioritize keeping layouts as Server Components to reduce bundle size and improve First Contentful Paint.

## 2025-02-18 - [Backend Schema Incompleteness Impact]
**Learning:** The `ScriptResponse` backend schema omitted `created_at` and `updated_at`, forcing the frontend to instantiate `new Date()` within render loops to display timestamps. This causes unnecessary re-renders (if not memoized) and incorrect "Last updated" values (always "now").
**Action:** When identifying frontend performance issues like unstable props (e.g., `new Date()`), trace the data source to the backend. If the field exists in the DB but is missing from the API response, prioritize updating the schema over frontend workarounds.
