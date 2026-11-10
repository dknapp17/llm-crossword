from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("http://localhost:8501")

    page.wait_for_selector("#exolve-frame")

    frame = page.frame_locator("#exolve-frame")
    clue = frame.locator(
        "#xlv2-across tr"
    ).filter(
        has=frame.locator(".xlv-clue-label").get_by_text(
            "32", exact=True
        )
    )

    clue.click()

    print("Exolve iframe found!")

    page.pause()

    # browser.close()