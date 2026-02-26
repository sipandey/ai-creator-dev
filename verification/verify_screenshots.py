from playwright.sync_api import sync_playwright

def verify_screenshots():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # Verify Login
            print("Visiting Login...")
            page.goto("http://localhost:3000/login")
            page.wait_for_selector("form", timeout=5000)
            page.screenshot(path="verification/login.png")
            print("Login screenshot taken.")

            # Verify Signup
            print("Visiting Signup...")
            page.goto("http://localhost:3000/signup")
            page.wait_for_selector("form", timeout=5000)
            page.screenshot(path="verification/signup.png")
            print("Signup screenshot taken.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_screenshots()
