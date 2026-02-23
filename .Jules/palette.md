## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-01 - Semantic Forms & Explicit Button Types
**Learning:** Native form submission (Enter key) is a critical expectation for login/signup flows. Without explicit `type="button"`, any button inside a `<form>` defaults to submit, causing accidental submissions (e.g., in toggle selectors).
**Action:** Always wrap inputs in a `<form>` tag with `onSubmit` preventing default, use `type="submit"` for primary actions, and explicitly set `type="button"` on all other interactive elements within the form.
