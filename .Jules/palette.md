## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-06 - Form Keyboard Submission
**Learning:** Auth components relied on `onClick` handlers and `div` wrappers, breaking native form submission via Enter key.
**Action:** Always wrap input groups in `<form onSubmit>` and use `type="submit"` buttons to ensure keyboard accessibility and native browser behavior.
