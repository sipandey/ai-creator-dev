## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-02 - Semantic Forms
**Learning:** `div`-wrapped inputs break Enter-key submission and assistive tech associations.
**Action:** Always wrap inputs in a `<form>` with `onSubmit`, use `htmlFor`/`id` for labels, and set `type="submit"` on the primary button.
