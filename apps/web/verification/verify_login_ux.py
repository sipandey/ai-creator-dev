from playwright.sync_api import sync_playwright, expect

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Navigating to login page...")
        # Navigate to login
        try:
            page.goto("http://localhost:3000/login")
        except Exception as e:
            print(f"Failed to navigate: {e}")
            return

        print("Waiting for form...")
        # Wait for form to be visible
        try:
            page.wait_for_selector("form", timeout=10000)
        except:
            print("Form not found!")
            page.screenshot(path="apps/web/verification/error_no_form.png")
            browser.close()
            return

        print("Verifying attributes...")
        # Verify inputs have required attribute
        email_input = page.locator("#email")
        password_input = page.locator("#password")

        expect(email_input).to_have_attribute("required", "")
        expect(password_input).to_have_attribute("required", "")

        # Verify button is type submit
        submit_button = page.get_by_role("button", name="Authorize Access")
        expect(submit_button).to_have_attribute("type", "submit")

        print("Verifying label association...")
        # Verify labels are linked
        # Click "Work Email" label and expect email input to be focused
        page.get_by_text("Work Email").click()
        expect(email_input).to_be_focused()

        page.get_by_text("Secure Password").click()
        expect(password_input).to_be_focused()

        print("Verifying submission via Enter key...")
        # Fill form and submit via Enter key
        email_input.fill("test@example.com")
        password_input.fill("password")
        password_input.press("Enter")

        # Wait a bit for potential submission feedback
        page.wait_for_timeout(2000)

        # Take screenshot of the form
        page.screenshot(path="apps/web/verification/login_form_verified.png")
        print("Screenshot taken.")

        browser.close()

if __name__ == "__main__":
    run()