## 2024-03-01 - React Form Accessibility and Semantics
**Learning:** In modern React applications using Tailwind/custom components, it's common to build forms relying solely on `onClick` handlers and detached labels for styling. This breaks basic accessibility and UX expectations:
1. Users cannot submit forms by pressing 'Enter'.
2. Clicking labels does not focus the associated input field, reducing the clickable hit area.
3. Custom radio buttons built with `div` or generic `button` tags lack inherent semantics (`role="radio"`, `aria-checked`, `role="radiogroup"`), rendering them invisible or confusing to screen reader users.
4. Non-submit buttons within a `<form>` will trigger a default submission if not explicitly typed with `type="button"`.

**Action:**
1. Always wrap input fields in a proper semantic `<form>` tag with an `onSubmit` handler to catch both button clicks and 'Enter' key presses.
2. Link `<label>` tags explicitly to their respective inputs using `htmlFor` and `id` properties.
3. For custom interactive components like stylized radio buttons, always enforce standard ARIA roles (`role="radio"`, `aria-checked`) and group them within a `role="radiogroup"` container.
4. Ensure primary action buttons use `type="submit"` and all secondary interactive buttons within the form use `type="button"`.