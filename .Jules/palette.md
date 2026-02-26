## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-02 - Semantic Form Structure
**Learning:** Auth forms were using `div` wrappers, breaking keyboard submission (Enter key) and screen reader label association.
**Action:** Always wrap inputs in a `<form>` tag with `onSubmit` preventing default, use `type="submit"` for primary actions, and explicitly link labels to inputs via `htmlFor` and `id`.

## 2026-02-02 - Multi-Button Form Safety
**Learning:** Interactive selector cards implemented as `<button>` elements inside a form context triggered accidental submissions because they lacked an explicit `type`.
**Action:** In multi-button forms, explicitly set `type="button"` on non-submit buttons (e.g., toggles, selectors) to prevent accidental form submission.
