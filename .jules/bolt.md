## 2025-02-18 - [Root Layout Optimization]
**Learning:** The root layout (`apps/web/app/layout.tsx`) was marked with `"use client"` despite having no interactive hooks or state. This caused the entire application shell to be included in the client-side JavaScript bundle unnecessarily.
**Action:** Audit all `layout.tsx` files for unnecessary `"use client"` directives. Prioritize keeping layouts as Server Components to reduce bundle size and improve First Contentful Paint.

## 2025-02-18 - [Missing Foreign Key Indexes]
**Learning:** Core models (`Script`, `CreatorPersona`, `ContentStrategy`) lacked database indexes on `user_id`, despite being the primary filter for multi-tenant queries. This leads to sequential scans instead of indexed lookups.
**Action:** Always verify `index=True` on `ForeignKey` columns in SQLAlchemy models, especially for high-cardinality tenant keys. Also, consider enabling GZip middleware for large JSON payloads (`script_json`).
