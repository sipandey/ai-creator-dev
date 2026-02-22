## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-10-18 - Semantic Auth Forms
**Learning:** Auth forms (`LoginForm`, `SignupForm`) relied on `div` wrappers and `onClick` handlers, breaking native "Enter to submit" behavior and accessibility.
**Action:** Always wrap input groups in a semantic `<form>` tag with `onSubmit` handlers to ensure keyboard accessibility and screen reader support by default.
