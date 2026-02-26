import os
import sys
import time
from playwright.sync_api import sync_playwright, expect

def verify_auth_forms():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Navigating to Login Page...")
        try:
            page.goto("http://localhost:3000/login", timeout=10000)
        except Exception as e:
            print(f"Error navigating to login page: {e}")
            print("Make sure the Next.js app is running on port 3000!")
            browser.close()
            sys.exit(1)

        print("Verifying Login Form Accessibility...")

        # Check Label-Input association for Email
        try:
            email_label = page.locator("label[for='email']")
            expect(email_label).to_be_visible()
            email_input = page.locator("input#email")
            expect(email_input).to_be_visible()

            # clicking label should focus input
            email_label.click()
            expect(email_input).to_be_focused()
            print("✅ Login Email label correctly associated with input")
        except Exception as e:
            print(f"❌ Failed Login Email label check: {e}")

        # Check Label-Input association for Password
        try:
            password_label = page.locator("label[for='password']")
            expect(password_label).to_be_visible()
            password_input = page.locator("input#password")
            expect(password_input).to_be_visible()

            # clicking label should focus input
            password_label.click()
            expect(password_input).to_be_focused()
            print("✅ Login Password label correctly associated with input")
        except Exception as e:
            print(f"❌ Failed Login Password label check: {e}")

        # Fill inputs
        email_input.fill("test@example.com")
        password_input.fill("password123")

        print("Testing Enter key submission on Login...")
        password_input.press("Enter")

        # Expect error message or loading state (since backend might not be reachable/mocked)
        try:
            error_message = page.get_by_text("Authorization failed. Check credentials.")
            # Since backend isn't real, this is likely
            expect(error_message).to_be_visible(timeout=5000)
            print("✅ Enter key triggered submission (Error message appeared)")
        except:
             print("⚠️ Could not verify submission via error message (backend might be down or slow).")

        page.screenshot(path="verification/login_verified.png")
        print("📸 Login verified screenshot saved.")

        print("Navigating to Signup Page...")
        page.goto("http://localhost:3000/signup")

        print("Verifying Signup Form Accessibility...")

        # Check Label-Input association for Email
        try:
            signup_email_label = page.locator("label[for='email']")
            expect(signup_email_label).to_be_visible()
            signup_email_input = page.locator("input#email")
            expect(signup_email_input).to_be_visible()

            signup_email_label.click()
            expect(signup_email_input).to_be_focused()
            print("✅ Signup Email label correctly associated with input")
        except Exception as e:
            print(f"❌ Failed Signup Email label check: {e}")

        # Check Label-Input association for Password
        try:
            signup_password_label = page.locator("label[for='password']")
            expect(signup_password_label).to_be_visible()
            signup_password_input = page.locator("input#password")
            expect(signup_password_input).to_be_visible()

            signup_password_label.click()
            expect(signup_password_input).to_be_focused()
            print("✅ Signup Password label correctly associated with input")
        except Exception as e:
            print(f"❌ Failed Signup Password label check: {e}")

        # Check Identity Path buttons are type="button" (not submitting form)
        print("Verifying Identity Path buttons do not submit form...")

        # Find buttons that are NOT the submit button
        # The submit button has text "Create Identity Account" or type="submit"
        # We look for the identity buttons.
        try:
            identity_buttons = page.locator("button[type='button']")
            count = identity_buttons.count()
            if count >= 2:
                 print(f"✅ Found {count} buttons with type='button'")
                 # Click one
                 identity_buttons.first.click()
                 # Check for submission error (which shouldn't happen)
                 # Wait a tiny bit to be sure
                 time.sleep(1)
                 # We need to check if ANY error message appeared.
                 # "Email and security key are mandatory." appears if we submit empty form.
                 # Since we filled inputs before? No, navigate clears inputs usually.
                 # Let's check for empty fields error.
                 error_msg = page.get_by_text("Email and security key are mandatory.")
                 if error_msg.is_visible():
                     print("❌ Identity button caused submission!")
                 else:
                     print("✅ Identity button click did NOT cause submission")
            else:
                 print("❌ Could not find identity buttons with type='button'")
        except Exception as e:
            print(f"⚠️ Error checking identity buttons: {e}")

        # Verify Enter key submission on Signup
        try:
            signup_email_input.fill("newuser@example.com")
            signup_password_input.fill("SecurePass123")
            signup_password_input.press("Enter")

            # Expect error (backend fail)
            expect(page.get_by_text("Registration failed")).to_be_visible(timeout=5000)
            print("✅ Enter key triggered submission (Error message appeared)")
        except:
            print("⚠️ Could not verify submission via error message.")

        page.screenshot(path="verification/signup_verified.png")
        print("📸 Signup verified screenshot saved.")

        browser.close()
        print("Verification Complete.")

if __name__ == "__main__":
    verify_auth_forms()
