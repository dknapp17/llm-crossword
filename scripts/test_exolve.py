from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("http://localhost:8501")

    page.wait_for_selector("#exolve-frame", timeout=0)

    print("Waiting for Solve Puzzle...")

    page.wait_for_selector("#solve-requested", timeout=0)

    print("Solve requested!")

    frame = page.frame_locator("#exolve-frame")

    clue = frame.locator(
        '#xlv2-across tr:has(> td.xlv-clue-label:text-is("32"))'
    )

    clue.click()

    grid_input = frame.locator("#xlv2-grid-input")
    grid_input.press_sequentially("CEROS")

    page.pause()

    browser.close()