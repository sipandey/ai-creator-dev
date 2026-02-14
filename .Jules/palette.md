## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and verification.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-06 - Fixing Invalid HTML Nesting in CTA
**Learning:** Nesting interactive elements (like `Button`) inside `Link` creates invalid HTML and disrupts screen readers.
**Action:** Extract reusable styling logic (e.g., `buttonVariants`) into separate files (without `"use client"`) to apply button styles directly to `Link` components in Server Components.
