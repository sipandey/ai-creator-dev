## 2025-02-18 - [Root Layout Optimization]
**Learning:** The root layout (`apps/web/app/layout.tsx`) was marked with `"use client"` despite having no interactive hooks or state. This caused the entire application shell to be included in the client-side JavaScript bundle unnecessarily.
**Action:** Audit all `layout.tsx` files for unnecessary `"use client"` directives. Prioritize keeping layouts as Server Components to reduce bundle size and improve First Contentful Paint.

## 2026-02-21 - [Missing Foreign Key Indexes]
**Learning:** SQLAlchemy models using `ForeignKey` do not automatically create database indexes on the foreign key column. This leads to full table scans when filtering by the foreign key (e.g., `user_id`), which is a critical performance bottleneck in multi-tenant applications.
**Action:** Explicitly add `index=True` to all `ForeignKey` columns in SQLAlchemy models, especially `user_id`, to ensure efficient tenant-scoped queries.
