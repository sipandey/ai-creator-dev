## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-05-23 - Semantic Forms for Accessibility
**Learning:** Using `<div>` wrappers and `onClick` handlers for forms breaks basic browser functionality like "Enter to submit" and password manager support, severely impacting usability.
**Action:** Always wrap inputs in a `<form>` tag, use `htmlFor`/`id` for label association, and ensure the primary button is `type="submit"`.
