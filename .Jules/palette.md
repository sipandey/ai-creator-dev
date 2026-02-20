## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-02 - Navigation Semantics
**Learning:** Using `button` + `useRouter.push` for navigation breaks native browser behavior (middle-click, SEO) and accessibility (screen readers don't see links).
**Action:** Always use `Link` for internal navigation and add `aria-current="page"` to the active item for screen readers.
