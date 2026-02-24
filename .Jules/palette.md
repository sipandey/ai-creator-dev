## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-04 - Semantic Forms for Accessibility
**Learning:** Using `div` wrappers with `onClick` handlers for form submission breaks native keyboard navigation (Enter key) and password manager integration.
**Action:** Always wrap input fields in a `<form>` element with `onSubmit` handling, use `type="submit"` buttons, and link labels to inputs via `htmlFor`/`id`.
