## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-01 - Semantic Forms
**Learning:** Using `div`s for inputs prevents password managers from working and breaks keyboard submission (Enter key).
**Action:** Always wrap inputs in a `<form>` tag with `onSubmit` handler, and ensure `label`s use `htmlFor` to connect to `input` `id`s.
