## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-05 - Invalid HTML Nesting (Button in Link)
**Learning:** Nesting `<Button>` inside `<Link>` creates invalid HTML (`<a href...><button...></button></a>`) and confusing accessibility.
**Action:** Use `buttonVariants` to style the `<Link>` directly, ensuring semantic correctness while maintaining visual consistency.
