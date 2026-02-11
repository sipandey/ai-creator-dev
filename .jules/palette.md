## 2026-02-11 - [Accessibility] Custom Slider Focus States
**Learning:** For custom slider components that use a hidden input, standard `:focus` styles on the input are invisible. Using `focus-within` on the parent container (which wraps both the hidden input and the custom visual track) is a clean way to show focus states without needing complex sibling selectors or JavaScript event listeners.
**Action:** When styling custom form controls with hidden native inputs, always check if the container can use `focus-within` to provide the visual focus indicator.
