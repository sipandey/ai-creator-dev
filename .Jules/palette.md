## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-02 - Semantic Forms for Accessibility
**Learning:** Using `div` wrappers instead of `<form>` tags breaks native browser behaviors (Enter to submit) and accessibility (screen readers).
**Action:** Always wrap input groups in a `<form>`, use `htmlFor`/`id` to link labels, and ensure auxiliary buttons inside forms have `type="button"`.
