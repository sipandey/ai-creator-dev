## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-18 - Semantic Form Structure
**Learning:** Wrapping inputs in `<form>` and using proper `type="submit"` buttons is critical not just for accessibility, but for basic usability like "Enter to submit". This was missing in Auth forms, leading to a "click-only" experience.
**Action:** Always wrap interactive input groups in `<form>` tags and ensure labels are programmatically associated via `htmlFor`/`id`.
