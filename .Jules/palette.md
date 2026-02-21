## 2026-02-01 - Standardized Button Loading State
**Learning:** Inconsistent loading states (replacing text with dots vs. spinner) harm UX and code maintainability.
**Action:** Always bake `isLoading` props into core interactive components like `Button` to ensure consistent feedback (spinner + disabled state) and reduce ad-hoc implementation in forms.

## 2026-02-02 - Context-Aware Action Buttons
**Learning:** Reusable action buttons (like Copy) need high-contrast overrides when placed in dark-themed cards within a light-themed app.
**Action:** Ensure utility components accept `className` props to support `!important` overrides for color context, or use CSS variables for theming.
