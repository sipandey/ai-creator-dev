## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-19 - Semantic Forms & Accessibility
**Learning:** Inputs without `<form>` wrappers break keyboard navigation (Enter to submit). Missing `htmlFor` on labels breaks accessibility for screen readers.
**Action:** Always wrap input groups in a `<form>`, use `type="submit"` for the primary action, and ensure every label has a matching `htmlFor` pointing to the input's `id`.
