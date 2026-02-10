## 2025-02-18 - [Root Layout Optimization]
**Learning:** The root layout (`apps/web/app/layout.tsx`) was marked with `"use client"` despite having no interactive hooks or state. This caused the entire application shell to be included in the client-side JavaScript bundle unnecessarily.
**Action:** Audit all `layout.tsx` files for unnecessary `"use client"` directives. Prioritize keeping layouts as Server Components to reduce bundle size and improve First Contentful Paint.

## 2025-02-18 - [Backend Index Optimization]
**Learning:** SQLite has stricter limitations for migrations than Postgres (e.g., no `ALTER COLUMN` without batch mode, no `now()` function). To enable local verification of migrations using SQLite, historical migrations must use SQLAlchemy generic functions (`sa.func.now()`) and `op.batch_alter_table`.
**Action:** Always write migrations using dialect-agnostic SQLAlchemy constructs where possible to support lightweight local verification and testing.
