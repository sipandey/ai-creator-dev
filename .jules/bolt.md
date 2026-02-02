## 2025-02-18 - [Root Layout Optimization]
**Learning:** The root layout (`apps/web/app/layout.tsx`) was marked with `"use client"` despite having no interactive hooks or state. This caused the entire application shell to be included in the client-side JavaScript bundle unnecessarily.
**Action:** Audit all `layout.tsx` files for unnecessary `"use client"` directives. Prioritize keeping layouts as Server Components to reduce bundle size and improve First Contentful Paint.

## 2025-02-18 - [API Request Caching Bug]
**Learning:** The `apiFetch` utility in `apps/web/services/api.ts` implements a naive request deduplication cache that uses `${method}:${path}` as the key. Crucially, it IGNORES the request body for POST/PUT requests. This means calling `POST /login` with different credentials sequentially returns the cached result of the first request!
**Action:** Fix `api.ts` to only cache safe methods (GET, HEAD) or include the body in the cache key (though caching mutations is generally discouraged). Disable caching for non-idempotent methods immediately.
