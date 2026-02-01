## 2025-02-18 - [Root Layout Optimization]
**Learning:** The root layout (`apps/web/app/layout.tsx`) was marked with `"use client"` despite having no interactive hooks or state. This caused the entire application shell to be included in the client-side JavaScript bundle unnecessarily.
**Action:** Audit all `layout.tsx` files for unnecessary `"use client"` directives. Prioritize keeping layouts as Server Components to reduce bundle size and improve First Contentful Paint.

## 2025-02-18 - [Lazy Loading Backend Services]
**Learning:** FastAPI `Depends` instantiates dependencies on every request. Heavy service initialization (like creating `httpx.AsyncClient` or loading ML models) in `__init__` kills performance for lightweight endpoints that don't use those heavy parts.
**Action:** Use lazy loading (properties) for heavy sub-services in request-scoped dependencies.
