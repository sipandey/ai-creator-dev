## 2025-02-18 - [Root Layout Optimization]
**Learning:** The root layout (`apps/web/app/layout.tsx`) was marked with `"use client"` despite having no interactive hooks or state. This caused the entire application shell to be included in the client-side JavaScript bundle unnecessarily.
**Action:** Audit all `layout.tsx` files for unnecessary `"use client"` directives. Prioritize keeping layouts as Server Components to reduce bundle size and improve First Contentful Paint.

## 2025-02-19 - [Missing Database Indexes on Foreign Keys]
**Learning:** Foreign key columns (`user_id`) on SQLAlchemy models `Feedback` and `Preference` were lacking database indexes. Because these tables are frequently queried in tenant-scoped filtering, the missing indexes could lead to full table scans and degraded backend performance over time.
**Action:** Always verify that foreign key columns intended for filtering are explicitly configured with `index=True` (`mapped_column(ForeignKey(...), index=True)`) in SQLAlchemy models.
