## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-02 - Flexible Core Components Enable Consistency
**Learning:** Ad-hoc buttons often exist because core components lack styling flexibility (e.g., icon colors).
**Action:** Enhance core components with flexible props like `iconClassName` instead of building custom one-off elements, ensuring accessibility and state management (loading) are inherited.
