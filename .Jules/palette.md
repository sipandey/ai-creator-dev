## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-05-21 - Semantic Forms
**Learning:** Missing `<form>` tags and label associations break keyboard submission and password managers.
**Action:** Always wrap input groups in a `<form>` tag and use `htmlFor`/`id` pairs to ensure accessibility and proper browser autofill behavior.
