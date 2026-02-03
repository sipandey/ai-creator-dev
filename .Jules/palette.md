## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-03 - Form Label Association
**Learning:** Visual labels without programmatic association (`htmlFor` + `id`) fail accessibility checks and prevent screen readers from announcing inputs correctly.
**Action:** Always use `htmlFor` on labels and matching `id` on inputs, even if they are wrapped in a div. Add `autoComplete` attributes to help password managers.
