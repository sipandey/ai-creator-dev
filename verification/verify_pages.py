from playwright.sync_api import sync_playwright, expect

def verify_pages():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Landing Page
        print("Visiting Landing Page...")
        page.goto("http://localhost:3000/")
        expect(page.get_by_role("heading", name="Scale your")).to_be_visible()
        # Verify the button exists and contains text
        button = page.get_by_role("button", name="Initialize Engine")
        expect(button).to_be_visible()
        page.screenshot(path="verification/landing_page.png")
        print("Landing Page Verified.")

        # 2. About Page
        print("Visiting About Page...")
        page.goto("http://localhost:3000/about")
        expect(page.get_by_role("heading", name="Creator AI")).to_be_visible()
        page.screenshot(path="verification/about_page.png")
        print("About Page Verified.")

        # 3. Signup Page
        print("Visiting Signup Page...")
        page.goto("http://localhost:3000/signup")
        # Signup form should be visible (it's client side rendered, might take a moment)
        expect(page.get_by_role("button", name="Create Identity Account")).to_be_visible()
        page.screenshot(path="verification/signup_page.png")
        print("Signup Page Verified.")

        browser.close()

if __name__ == "__main__":
    try:
        verify_pages()
        print("All verifications passed.")
    except Exception as e:
        print(f"Verification failed: {e}")
        exit(1)
