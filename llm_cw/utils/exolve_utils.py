from playwright.sync_api import Page

from llm_cw.domain.crossword import AcrossDown


class ExolveController:
    def __init__(self, page: Page):
        self.page = page
        self.frame = page.frame_locator("#exolve-frame")

    def select_clue(self, direction: AcrossDown, number: int) -> None:
        clue = self.frame.locator(
            f'#xlv2-{direction.value} tr:has(> td.xlv-clue-label:text-is("{number}"))'
        )

        clue.click()

    def enter_answer(self, answer: str) -> None:
        grid_input = self.frame.locator("#xlv2-grid-input")
        grid_input.press_sequentially(answer, delay=100)  # Add a delay of 100ms between key presses
