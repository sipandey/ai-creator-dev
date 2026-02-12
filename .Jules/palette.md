## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-12 - Semantic Forms for Accessibility
**Learning:** Wrapping inputs in a `<form>` element with `onSubmit` is crucial for keyboard users (Enter to submit) and password managers (auto-fill).
**Action:** Always refactor `div`-based forms to semantic `<form>` elements with explicit `htmlFor`/`id` associations and `type="submit"` buttons.
