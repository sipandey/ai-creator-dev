## 2025-02-18 - [Root Layout Optimization]
**Learning:** The root layout (`apps/web/app/layout.tsx`) was marked with `"use client"` despite having no interactive hooks or state. This caused the entire application shell to be included in the client-side JavaScript bundle unnecessarily.
**Action:** Audit all `layout.tsx` files for unnecessary `"use client"` directives. Prioritize keeping layouts as Server Components to reduce bundle size and improve First Contentful Paint.

## 2025-02-19 - [SQLAlchemy Foreign Key Indexing]
**Learning:** In SQLAlchemy, foreign key columns (`ForeignKey`) are not indexed by default. This can cause significant performance bottlenecks and N+1 query-like slow downs for tenant-scoped data since these foreign keys (like `user_id` or `creator_id`) are frequently used for filtering.
**Action:** Always add `index=True` explicitly when defining foreign key columns in SQLAlchemy models, unless there's a specific reason not to index them. Ensure corresponding alembic migrations include `op.create_index`.
