import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        # Set auth token in localStorage
        page.add_init_script("localStorage.setItem('token', 'fake-token');")

        # Mock /script API response
        page.route("**/script", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='[{"id": 1, "user_id": 1, "topic": "Test Script", "script_json": {"hook": "Amazing hook"}, "status": "DRAFT"}, {"id": 2, "user_id": 1, "topic": "Another Script", "script_json": {"hook": "Another hook"}, "status": "PUBLISHED"}]'
        ))

        print("Navigating to /scripts...")
        try:
            page.goto("http://localhost:3000/scripts", wait_until="networkidle")
        except Exception as e:
            print(f"Navigation failed: {e}")

        # Wait for content
        try:
            page.wait_for_selector("text=Test Script", timeout=10000)
            print("Found 'Test Script'")
        except Exception as e:
            print(f"Timeout waiting for selector: {e}")
            page.screenshot(path="verification/error_screenshot.png")
            print("Saved error screenshot")
            browser.close()
            return

        # Check if scripts are rendered as links
        # ScriptCard renders <Link href="/script?id=...">
        links = page.locator('a[href*="/script?id="]')
        count = links.count()
        print(f"Found {count} script links")

        if count == 2:
            print("SUCCESS: Scripts are rendered as links.")
        else:
            print(f"FAILURE: Expected 2 links, found {count}.")

        page.screenshot(path="verification/success_screenshot.png")
        print("Saved success screenshot")
        browser.close()

if __name__ == "__main__":
    run()
