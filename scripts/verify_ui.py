import os
from playwright.sync_api import sync_playwright

os.makedirs("/home/jules/verification/videos", exist_ok=True)
os.makedirs("/home/jules/verification/screenshots", exist_ok=True)

def run_cuj(page):
    page.goto("http://localhost:3000")
    page.wait_for_timeout(1000)

    # Search interaction
    search_input = page.get_by_placeholder("Поиск по названию, МНН (Парацетамол), фармгруппе, ATC или показанию...")
    search_input.fill("Парацетамол")
    page.wait_for_timeout(1000)

    # Click on search result
    page.get_by_role("link", name="Парацетамол Таблетки", exact=True).click()
    page.wait_for_timeout(1500)

    # Take screenshot of Drug Details
    page.screenshot(path="/home/jules/verification/screenshots/verification.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
