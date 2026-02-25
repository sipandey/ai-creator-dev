## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-25 - Loading States in Custom Buttons
**Learning:** When refactoring highly-styled custom buttons to add loading states, replacing them with a shared `Button` component may cause visual regression (e.g., lost icon colors defined via classes).
**Action:** In such cases, implement the standardized loading pattern (spinner replacing icon + disabled state) manually within the custom component to preserve design fidelity while improving UX.
