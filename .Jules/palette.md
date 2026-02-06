## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2025-02-18 - Semantic Form Submission
**Learning:** Users expect the "Enter" key to submit forms, but `div`-based inputs break this behavior and require explicit `onKeyDown` handlers.
**Action:** Always wrap input groups in a `<form>` tag with a submit button to get native "Enter" key submission and accessibility benefits for free.
