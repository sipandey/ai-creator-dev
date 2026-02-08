## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-01 - Form Encapsulation in Cards
**Learning:** `CardContent` typically applies vertical spacing (`space-y`). When checking accessibility by wrapping inputs in a `<form>`, this spacing context breaks if not transferred.
**Action:** When migrating to semantic forms, move `space-y-*` classes from the parent container to the `<form>` element to preserve vertical rhythm.
