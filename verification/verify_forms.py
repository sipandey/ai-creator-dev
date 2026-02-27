from playwright.sync_api import sync_playwright

def verify_forms():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Navigating to Signup Page...")
        # Since we don't have a running server, we'll assume the verification
        # is static analysis or needs the dev server running.
        # For this environment, I'll start the dev server in the background
        # but first I need to check if I can access the page.

        # NOTE: In this specific environment, I will try to start the dev server
        # in a separate process if one isn't running, but for this script
        # I will assume port 3000 is available after I start it.

        try:
            page.goto("http://localhost:3000/signup", timeout=60000)

            # 1. Verify Signup Form Structure
            print("Verifying Signup Form...")
            # Check for the form element
            if page.locator("form").count() > 0:
                print("✅ Signup Form element found")
            else:
                print("❌ Signup Form element NOT found")

            # Check for button types
            # The submit button should be type="submit"
            submit_btn = page.locator("button[type='submit']")
            if submit_btn.count() > 0:
                print(f"✅ Found {submit_btn.count()} submit button(s)")
            else:
                print("❌ No submit button found")

            # The identity path buttons should be type="button"
            # We can find them by the text content or icon,
            # but let's look for buttons inside the form that are NOT submit
            buttons = page.locator("form button:not([type='submit'])")
            count = buttons.count()
            print(f"Found {count} non-submit buttons in form")

            all_good = True
            for i in range(count):
                btn = buttons.nth(i)
                btn_type = btn.get_attribute("type")
                if btn_type == "button":
                    print(f"✅ Button {i} has type='button'")
                else:
                    print(f"❌ Button {i} has type='{btn_type}' (expected 'button')")
                    all_good = False

            page.screenshot(path="verification/signup_form.png")
            print("📸 Signup screenshot saved to verification/signup_form.png")

        except Exception as e:
            print(f"Error visiting signup: {e}")

        try:
            print("\nNavigating to Login Page...")
            page.goto("http://localhost:3000/login", timeout=60000)

            # 2. Verify Login Form Structure
            print("Verifying Login Form...")
            if page.locator("form").count() > 0:
                print("✅ Login Form element found")
            else:
                print("❌ Login Form element NOT found")

            submit_btn = page.locator("button[type='submit']")
            if submit_btn.count() > 0:
                print(f"✅ Found {submit_btn.count()} submit button(s)")
            else:
                print("❌ No submit button found")

            page.screenshot(path="verification/login_form.png")
            print("📸 Login screenshot saved to verification/login_form.png")

        except Exception as e:
            print(f"Error visiting login: {e}")

        browser.close()

if __name__ == "__main__":
    verify_forms()
