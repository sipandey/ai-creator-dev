## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2025-05-23 - Semantic Forms for Accessibility
**Learning:** Wrapping inputs in `<form>` and associating labels with `htmlFor` is critical for screen readers and keyboard users (Enter to submit).
**Action:** Always wrap input groups in `<form>` and ensure every `input` has a corresponding `label` with matching `for`/`id` attributes.
