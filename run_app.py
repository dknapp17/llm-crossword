import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

from llm_cw.domain.crossword import AcrossDown
from llm_cw.solvers.toy_solver import ToySolver
from llm_cw.utils.exolve_utils import ExolveController

signal_file = Path("solve_requested.txt")
signal_file.unlink(missing_ok=True)


log_file = Path("solver_log.txt")
log_file.write_text("")


def log_message(message: str) -> None:
    with log_file.open("a", encoding="utf-8") as f:
        f.write(message + "\n")

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
        controller = ExolveController(page)

        page.goto("http://localhost:8501", timeout=120000)

        print("Streamlit is running under Playwright control.")

        print("Waiting for Solve Puzzle...")

        while not signal_file.exists():
            time.sleep(0.2)

        signal_file.unlink()

        log_message("Solve requested!")

        solver_config = controller.get_solver_config()
        solver = ToySolver(config=solver_config)

        frame = page.frame_locator("#exolve-frame")

        # Assumes every puzzle has a 1 across
        controller.select_clue(AcrossDown.ACROSS, 1)
        puzzle_complete = False

        while not puzzle_complete:
            current_clue = controller.read_current_clue()
            answer = solver.solve_clue(current_clue)

            if answer.confidence > 0.1:
                controller.enter_answer(answer.text)
                log_message(
                    f"High confidence ({answer.confidence:.2f}) - entering answer "
                    f"for {current_clue.number}{current_clue.direction}"
                )
            else:
                log_message(
                    f"Low confidence ({answer.confidence:.2f}) - skipping answer for "
                    f"{current_clue.number}{current_clue.direction}"
                )

            puzzle_complete = controller.is_puzzle_filled()

            if not puzzle_complete:
                controller.select_next_incomplete_clue()

        if puzzle_complete:
            log_message("All squares are filled in!")


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