from playwright.sync_api import sync_playwright

def verify_landing_page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            print("Navigating to landing page...")
            page.goto("http://localhost:3000")

            # Wait for content to load
            page.wait_for_selector("text=Scale your")

            print("Checking for 'Initialize Engine' link...")
            # It should be a link now
            link = page.get_by_role("link", name="Initialize Engine")
            if link.is_visible():
                print("SUCCESS: 'Initialize Engine' is a link.")
            else:
                print("FAILURE: 'Initialize Engine' link not found.")

            # It should NOT be a button (this was the issue: button inside link)
            # However, if it's just a styled link, it won't be a button role.
            # If it was nested, it would have been a button inside a link.
            # But the inner button would have role="button".
            button = page.get_by_role("button", name="Initialize Engine")
            if button.is_visible():
                print("FAILURE: 'Initialize Engine' is still recognized as a button (nested?).")
            else:
                print("SUCCESS: 'Initialize Engine' is NOT a button.")

            # Take screenshot
            page.screenshot(path="verification/landing_page_fix.png")
            print("Screenshot saved to verification/landing_page_fix.png")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_landing_page()
