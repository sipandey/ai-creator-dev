## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-18 - Semantic Forms & Submission
**Learning:** Forms relying on div containers instead of semantic form elements cause accessibility issues (no label focus) and poor usability (Enter key doesn't submit).
**Action:** Always wrap inputs in a `<form>` tag with an `onSubmit` handler, and ensure buttons are `type="submit"` to enable native browser behaviors like "Enter to submit".
