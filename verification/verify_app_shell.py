from playwright.sync_api import sync_playwright, expect

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        # Inject token to simulate logged-in state
        page = context.new_page()
        page.add_init_script("""
            localStorage.setItem('token', 'dummy-token');
        """)

        print("Navigating to dashboard...")
        page.goto("http://localhost:3000/dashboard")

        # Wait for AppShell to load
        # Check for the brand header "Creator AI"
        print("Waiting for AppShell...")
        expect(page.get_by_text("Creator AI")).to_be_visible()

        # Check for navigation links
        print("Checking navigation links...")

        # Blueprint link
        blueprint_link = page.get_by_role("link", name="Blueprint")
        expect(blueprint_link).to_be_visible()
        expect(blueprint_link).to_have_attribute("href", "/strategy")

        # Editor link
        editor_link = page.get_by_role("link", name="Editor")
        expect(editor_link).to_be_visible()
        expect(editor_link).to_have_attribute("href", "/script")

        # Hub link (central button)
        hub_link = page.get_by_role("link", name="Production Hub")
        expect(hub_link).to_be_visible()
        expect(hub_link).to_have_attribute("href", "/dashboard")
        expect(hub_link).to_have_attribute("aria-current", "page") # Should be active on dashboard

        # Take screenshot
        print("Taking screenshot...")
        page.screenshot(path="/home/jules/verification/app_shell_verification.png")

        browser.close()
        print("Verification complete!")

if __name__ == "__main__":
    run()
