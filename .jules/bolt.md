## 2025-02-18 - [Root Layout Optimization]
**Learning:** The root layout (`apps/web/app/layout.tsx`) was marked with `"use client"` despite having no interactive hooks or state. This caused the entire application shell to be included in the client-side JavaScript bundle unnecessarily.
**Action:** Audit all `layout.tsx` files for unnecessary `"use client"` directives. Prioritize keeping layouts as Server Components to reduce bundle size and improve First Contentful Paint.

## 2025-01-28 - [Tenant Isolation Performance]
**Learning:** Found critical N+1 query vulnerability in `scripts` and `content_strategies` tables. `user_id` foreign keys were missing indexes, causing full table scans for all user-scoped queries.
**Action:** Always add `index=True` to foreign key columns in multi-tenant models, especially `user_id`, to ensure O(log n) lookup performance.
