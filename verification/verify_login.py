from playwright.sync_api import sync_playwright, expect
import time

def verify_login(page):
    print("Navigating to login page...")
    page.goto("http://localhost:3000/login")

    # Wait for the page to load
    page.wait_for_selector("text=Welcome back", timeout=10000)

    print("Taking after screenshot...")
    page.screenshot(path="verification/login_after.png")

    # Fill in credentials
    print("Filling credentials...")
    page.fill("input[type='email']", "test@example.com")
    page.fill("input[type='password']", "password123")

    # Check for form role
    try:
        page.locator("form").wait_for(state="attached", timeout=2000)
        print("✅ Form element found!")
    except:
        print("❌ No form element found")
        raise Exception("Form element not found")

    # Attempt to submit via Enter key
    print("Pressing Enter in password field...")
    page.focus("input[type='password']")

    submitted = False
    try:
        # Wait for a request to /auth/login
        # Now we expect this to SUCCEED (initiate the request)
        with page.expect_request(lambda request: "/auth/login" in request.url, timeout=3000):
            page.keyboard.press("Enter")
        submitted = True
        print("✅ Form submitted via Enter key!")
    except Exception as e:
        print(f"❌ Form NOT submitted via Enter key. Error: {e}")
        raise e

    # Check for labels
    try:
        # Use get_by_label which requires id/htmlFor association to work
        page.get_by_label("Work Email").click()
        print("✅ 'Work Email' label correctly associated with input")

        page.get_by_label("Secure Password").click()
        print("✅ 'Secure Password' label correctly associated with input")
    except Exception as e:
        print(f"❌ Label association failed: {e}")
        raise e

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_login(page)
        except Exception as e:
            print(f"Test failed with error: {e}")
            page.screenshot(path="verification/error.png")
            exit(1)
        finally:
            browser.close()
