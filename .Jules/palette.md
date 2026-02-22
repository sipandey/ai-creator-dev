## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-22 - Semantic Navigation with Next.js Link
**Learning:** Using <button> with router.push() for navigation breaks accessibility and native browser features (e.g. open in new tab).
**Action:** Always use Next.js <Link> for internal navigation, applying button styles directly to the Link component if needed.
