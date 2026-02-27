from playwright.sync_api import sync_playwright, expect

def verify_login_password_toggle():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            print("Navigating to login page...")
            page.goto("http://localhost:3000/login")

            # Wait for the password field to be visible
            password_input = page.locator('input[placeholder="••••••••"]')
            password_input.wait_for(state="visible")

            # Fill in some text
            print("Filling password...")
            password_input.fill("secret123")

            # Check initial state (should be type="password")
            print("Checking initial state...")
            expect(password_input).to_have_attribute("type", "password")

            # Take a screenshot masked
            page.screenshot(path="verification/login_masked.png")
            print("Screenshot saved to verification/login_masked.png")

            # Find the toggle button
            toggle_button = page.get_by_label("Show password")

            # Click the toggle button
            print("Clicking toggle button...")
            toggle_button.click()

            # Check toggled state (should be type="text")
            print("Checking toggled state...")
            expect(password_input).to_have_attribute("type", "text")

            # Take a screenshot visible
            page.screenshot(path="verification/login_visible.png")
            print("Screenshot saved to verification/login_visible.png")

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    verify_login_password_toggle()