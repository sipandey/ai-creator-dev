## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-18 - Semantic Form Structure
**Learning:** Auth forms relied on `div`s and `onClick` handlers, breaking standard browser behaviors (Enter to submit, password managers).
**Action:** Always wrap input groups in `<form>` tags with explicit `id`/`htmlFor` pairs and `type="submit"` buttons to ensure accessibility and browser feature support.
