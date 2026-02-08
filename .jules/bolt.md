## 2025-02-18 - [Root Layout Optimization]
**Learning:** The root layout (`apps/web/app/layout.tsx`) was marked with `"use client"` despite having no interactive hooks or state. This caused the entire application shell to be included in the client-side JavaScript bundle unnecessarily.
**Action:** Audit all `layout.tsx` files for unnecessary `"use client"` directives. Prioritize keeping layouts as Server Components to reduce bundle size and improve First Contentful Paint.

## 2025-02-18 - [Incorrect API Caching]
**Learning:** The `apiFetch` utility (`apps/web/services/api.ts`) caches requests based only on `method` and `path`, ignoring the request body. This causes different POST requests (e.g., generating scripts with different topics) to return stale/incorrect cached data if called sequentially within the cache duration.
**Action:** When implementing request caching, always include a hash of the request body in the cache key for non-GET requests, or disable caching for mutation methods (POST, PUT, DELETE) unless idempotent behavior is guaranteed.
