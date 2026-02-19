import os
from playwright.sync_api import sync_playwright, expect

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        # Inject fake token
        page.add_init_script("""
            localStorage.setItem('token', 'fake-token');
        """)

        try:
            # Navigate to dashboard
            print("Navigating to /dashboard...")
            page.goto("http://localhost:3000/dashboard")

            # Wait for content to load
            # Wait for the navigation bar to be visible
            nav = page.locator("nav")
            expect(nav).to_be_visible(timeout=10000)

            print("Checking navigation links...")

            # Check the "Production Hub" link (central button)
            # Use role="link" and name from aria-label
            hub_link = page.get_by_role("link", name="Production Hub")
            expect(hub_link).to_be_visible()
            expect(hub_link).to_have_attribute("href", "/dashboard")

            # Check aria-current="page" on active link (Hub is active on /dashboard)
            expect(hub_link).to_have_attribute("aria-current", "page")
            print("Hub link verified (is active).")

            # Check "Blueprint" link
            # The text is "BLUEPRINT" (uppercase in CSS/HTML?), check code:
            # <span className="text-[9px] font-black uppercase tracking-tight">{item.label}</span>
            # item.label is "Blueprint".
            # get_by_role("link", name="Blueprint") should work if the text is accessible.
            blueprint_link = page.get_by_role("link", name="Blueprint")
            expect(blueprint_link).to_be_visible()
            expect(blueprint_link).to_have_attribute("href", "/strategy")

            # Should NOT have aria-current="page"
            expect(blueprint_link).not_to_have_attribute("aria-current", "page")
            print("Blueprint link verified (is inactive).")

            # Take screenshot of the bottom navigation
            screenshot_path = os.path.join(os.getcwd(), "verification/appshell_verification.png")
            nav.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/error.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    run()
