import os
from playwright.sync_api import sync_playwright, Page, expect

def test_loading_state(page: Page):
    # Mock backend API
    page.route("http://localhost:8000/script/1", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='''{
            "id": 1,
            "user_id": 1,
            "topic": "Test Topic",
            "script_json": {
                "hook": "Test Hook",
                "scenes": ["Scene 1", "Scene 2"],
                "audio_script": "Test Audio",
                "caption": "Test Caption",
                "cta": "Test CTA"
            },
            "status": "DRAFT"
        }'''
    ))

    # Mock feedback endpoint to hang
    page.route("http://localhost:8000/feedback", lambda route: None)

    # Set Auth Token
    print("Setting auth token...")
    page.goto("http://localhost:3000/login")
    page.evaluate("localStorage.setItem('token', 'dummy-token')")

    print("Navigating to script page...")
    page.goto("http://localhost:3000/script?id=1")

    print("Waiting for script content...")
    try:
        expect(page.get_by_text("Test Hook")).to_be_visible()
    except Exception as e:
        page.screenshot(path="/home/jules/verification/error_state_2.png")
        raise e

    print("Clicking Authorize button...")
    auth_btn = page.get_by_role("button", name="Authorize")

    # Scroll to button to ensure visibility
    auth_btn.scroll_into_view_if_needed()

    auth_btn.click()

    print("Waiting for loading state...")
    page.wait_for_timeout(500)

    print("Taking screenshot...")
    page.screenshot(path="/home/jules/verification/loading_state.png")
    print("Screenshot saved.")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_loading_state(page)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()
