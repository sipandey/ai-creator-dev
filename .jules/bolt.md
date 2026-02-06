## 2025-02-18 - [Root Layout Optimization]
**Learning:** The root layout (`apps/web/app/layout.tsx`) was marked with `"use client"` despite having no interactive hooks or state. This caused the entire application shell to be included in the client-side JavaScript bundle unnecessarily.
**Action:** Audit all `layout.tsx` files for unnecessary `"use client"` directives. Prioritize keeping layouts as Server Components to reduce bundle size and improve First Contentful Paint.

## 2025-02-18 - [Missing Database Indexes]
**Learning:** Core relationships (`CreatorPersona.user_id`, `Script.user_id`) were defined as Foreign Keys but lacked database indexes, leading to O(N) lookups for critical access patterns like fetching a user's profile.
**Action:** Always verify that foreign keys have explicit `index=True` (or `unique=True` for 1:1) in SQLAlchemy models, as Alembic/SQLAlchemy does not index them by default.
