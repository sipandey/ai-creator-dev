from playwright.sync_api import sync_playwright, expect

def test_login_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Mock the login API to return success
        page.route("**/auth/login", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"access_token": "fake-token", "token_type": "bearer"}'
        ))

        # Mock the persona API
        # If persona exists, it returns the persona object.
        # If I want to test redirect to dashboard, I should return a persona.
        page.route("**/persona/enhanced", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"id": 1, "name": "Test Persona"}'
        ))

        # Navigate to the login page
        print("Navigating to login page...")
        page.goto("http://localhost:3000/login")

        # Wait for the email input to be visible
        print("Waiting for email input...")
        email_input = page.wait_for_selector("input#email")

        # Verify labels are associated correctly
        email_label = page.locator("label[for='email']")
        expect(email_label).to_be_visible()

        # Fill in the form
        print("Filling in the form...")
        page.fill("input#email", "test@example.com")
        page.fill("input#password", "password123")

        # Submit by pressing Enter on the password field
        print("Submitting by pressing Enter...")
        page.press("input#password", "Enter")

        print("Waiting for navigation to dashboard...")
        try:
            page.wait_for_url("**/dashboard", timeout=10000)
            print("Successfully navigated to dashboard!")
        except Exception as e:
            print(f"Navigation failed or timed out: {e}")
            page.screenshot(path="verification/verification_failed.png")
            raise e

        # Take a success screenshot
        print("Taking screenshot...")
        page.screenshot(path="verification/verification.png")

        browser.close()

if __name__ == "__main__":
    test_login_form()
