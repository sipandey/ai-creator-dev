## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-18 - Semantic Forms & Polymorphic Links
**Learning:** React components that render interactive elements (like `<Button>`) nested inside other interactive elements (like `<Link>`) create invalid HTML5 and confuse screen readers. Visually identical components must be polymorphic or style-based to be accessible.
**Action:** Use `buttonVariants` on `<Link>` elements instead of wrapping `<Button>` inside, and always wrap inputs in semantic `<form>` tags to enable native keyboard submission and password manager support.
