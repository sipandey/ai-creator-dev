import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Navigating to login page...")
        try:
            page.goto("http://localhost:3000/login", timeout=60000) # Increased timeout for first load
        except Exception as e:
            print(f"Failed to load page: {e}")
            browser.close()
            return

        print("Checking for form element...")
        form = page.locator("form")
        if form.count() > 0:
            print("✅ Form element found.")
        else:
            print("❌ Form element NOT found.")

        print("Checking email input and label...")
        email_input = page.locator("input#email")
        email_label = page.locator("label[for='email']")

        if email_input.count() > 0:
            print("✅ Input with id='email' found.")
            autocomplete = email_input.get_attribute("autocomplete")
            if autocomplete == "email":
                print(f"✅ Email autocomplete correct: {autocomplete}")
            else:
                print(f"❌ Email autocomplete incorrect: {autocomplete}")
        else:
            print("❌ Input with id='email' NOT found.")

        if email_label.count() > 0:
            print("✅ Label with for='email' found.")
        else:
            print("❌ Label with for='email' NOT found.")

        print("Checking password input and label...")
        password_input = page.locator("input#password")
        password_label = page.locator("label[for='password']")

        if password_input.count() > 0:
            print("✅ Input with id='password' found.")
            autocomplete = password_input.get_attribute("autocomplete")
            if autocomplete == "current-password":
                print(f"✅ Password autocomplete correct: {autocomplete}")
            else:
                print(f"❌ Password autocomplete incorrect: {autocomplete}")
        else:
            print("❌ Input with id='password' NOT found.")

        if password_label.count() > 0:
            print("✅ Label with for='password' found.")
        else:
            print("❌ Label with for='password' NOT found.")

        # Check button type
        submit_button = page.locator("button[type='submit']")
        if submit_button.count() > 0:
            print("✅ Submit button found.")
        else:
            print("❌ Submit button NOT found.")

        page.screenshot(path="verification/login_a11y.png")
        print("Screenshot saved to verification/login_a11y.png")

        browser.close()

if __name__ == "__main__":
    run()
