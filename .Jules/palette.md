## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-01 - Semantic Form Structure
**Learning:** Auth forms were implemented as `div` wrappers, breaking keyboard submission (Enter key) and accessibility (screen readers, password managers).
**Action:** Always wrap inputs in a `<form>` tag, use `htmlFor`/`id` for labels, and explicit `autoComplete` attributes. Ensure secondary buttons inside forms have `type="button"`.
