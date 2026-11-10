import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

signal_file = Path("solve_requested.txt")
signal_file.unlink(missing_ok=True)

app = subprocess.Popen(
    [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "app/streamlit_app.py",
    ]
)

exolve_dir = Path("app/static/exolve")
existing_puzzles = set(exolve_dir.glob("*.puz"))

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("http://localhost:8501", timeout=120000)

        print("Streamlit is running under Playwright control.")

        print("Waiting for Solve Puzzle...")

        while not signal_file.exists():
            time.sleep(0.2)

        signal_file.unlink()

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

finally:
    app.terminate()
    app.wait()
    # Remove puzzles uploaded during this session
    new_puzzles = set(exolve_dir.glob("*.puz")) - existing_puzzles

    for puzzle in new_puzzles:
        puzzle.unlink(missing_ok=True)

    signal_file.unlink(missing_ok=True)