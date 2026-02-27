## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-12 - Semantic Forms & Interaction Safety
**Learning:** Using `<div>` wrappers for forms breaks standard browser behavior (enter-to-submit) and accessibility tools. Furthermore, using `<button>` elements for selection (like radio groups) inside a form without `type="button"` triggers accidental submissions.
**Action:** Always wrap inputs in a semantic `<form>` element. explicitly set `type="button"` on any interactive element inside a form that isn't the primary submit action.
