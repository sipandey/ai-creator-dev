## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-24 - Button-like Links
**Learning:** Nesting `<Button>` inside `<Link>` creates invalid HTML and can cause Next.js App Router errors when passing unserializable props (like icons).
**Action:** Apply `buttonVariants` directly to `<Link>` components instead of nesting, ensuring semantic validity and preventing hydration issues.
