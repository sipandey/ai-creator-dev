from playwright.sync_api import sync_playwright

def verify_a11y():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Login Page Verification
        print("Navigating to Login Page...")
        try:
            page.goto("http://localhost:3000/login", timeout=30000)
            page.wait_for_selector("form", timeout=10000)
            print("Form found on Login Page.")
        except Exception as e:
            print(f"Form not found on Login Page or navigation failed: {e}")
            browser.close()
            return

        # Check for inputs and labels
        try:
            email_input = page.locator("input#email")
            email_label = page.locator("label[for='email']")
            if email_input.count() > 0 and email_label.count() > 0:
                print("Email input and label association verified.")
            else:
                print("Email input or label missing!")

            password_input = page.locator("input#password")
            password_label = page.locator("label[for='password']")
            if password_input.count() > 0 and password_label.count() > 0:
                print("Password input and label association verified.")
            else:
                print("Password input or label missing!")

            submit_btn = page.locator("button[type='submit']")
            if submit_btn.count() > 0:
                print("Submit button verified.")
            else:
                print("Submit button missing!")
        except Exception as e:
            print(f"Error checking Login Page elements: {e}")

        page.screenshot(path="verification/login_verification.png")
        print("Login Page screenshot taken.")

        # Signup Page Verification
        print("Navigating to Signup Page...")
        try:
            page.goto("http://localhost:3000/signup", timeout=30000)
            page.wait_for_selector("form", timeout=10000)
            print("Signup Form found.")
        except Exception as e:
            print(f"Signup Form not found or navigation failed: {e}")

        # Check inputs
        try:
            if page.locator("input#email").count() > 0 and page.locator("label[for='email']").count() > 0:
                print("Signup Email input verified.")
            if page.locator("input#password").count() > 0 and page.locator("label[for='password']").count() > 0:
                print("Signup Password input verified.")
            if page.locator("button[type='submit']").count() > 0:
                print("Signup Submit button verified.")
            # Check type="button" on selectors
            selectors = page.locator("button[type='button']")
            print(f"Found {selectors.count()} type='button' elements.")
        except Exception as e:
            print(f"Error checking Signup Page elements: {e}")

        page.screenshot(path="verification/signup_verification.png")
        print("Signup Page screenshot taken.")

        # Landing Page Verification
        print("Navigating to Landing Page...")
        try:
            page.goto("http://localhost:3000/", timeout=30000)
            # Check if "Initialize Engine" is a Link (a tag)
            # It should be an anchor tag with text containing "Initialize Engine"
            link = page.get_by_role("link", name="Initialize Engine")
            if link.count() > 0:
                print("Initialize Engine is a link.")
                # Verify it has button classes (e.g. inline-flex)
                classes = link.get_attribute("class")
                if classes and "inline-flex" in classes:
                     print("Link has button styling.")
            else:
                print("Initialize Engine link not found!")
        except Exception as e:
            print(f"Error checking Landing Page elements: {e}")

        page.screenshot(path="verification/landing_verification.png")
        print("Landing Page screenshot taken.")

        browser.close()

if __name__ == "__main__":
    verify_a11y()
