## 2024-05-24 - Accessible Modal Dialog
**Learning:** Found that the Settings menu in the `AppShell` component lacked standard modal dialog attributes (`role="dialog"`, `aria-modal="true"`) and an `aria-label` for its close button. This is a common pattern for custom modals that prevents screen readers from announcing them properly.
**Action:** When creating or reviewing custom modals/dialogs, always ensure the container has `role="dialog"` and `aria-modal="true"`, and any icon-only buttons (like a Close "X") have descriptive `aria-label`s.
