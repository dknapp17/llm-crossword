from playwright.sync_api import Page

from llm_cw.domain.crossword import AcrossDown, SolverClueInput


class ExolveController:
    def __init__(self, page: Page):
        self.page = page
        self.frame = page.frame_locator("#exolve-frame")

    def select_clue(self, direction: AcrossDown, number: int) -> None:
        clue = self.frame.locator(
            f'#xlv2-{direction.value} tr:has(> td.xlv-clue-label:text-is("{number}"))'
        )

        clue.click()

    def select_next_clue(self) -> None:
        self.frame.locator("#xlv2-next").click(delay=500)

    def read_current_clue(self) -> SolverClueInput:
        clue_text = self.frame.locator(
            "#xlv2-curr-clue-text .xlv-clue-text-raw"
        ).text_content()

        cells = self.frame.locator(
            '#xlv2-grid g:has(rect[style*="rgb(255, 182, 180)"]), '
            '#xlv2-grid g:has(rect[style*="mistyrose"])'
        )

        positional_constraints = {}

        for i in range(cells.count()):
            letter = letter = cells.nth(i).locator(".xlv-cell-text").text_content()
            if letter:
                positional_constraints[i] = letter

        return SolverClueInput(
            text=clue_text.strip(),
            length=cells.count(),
            positional_constraints=positional_constraints,
        )

    def enter_answer(self, answer: str) -> None:
        grid_input = self.frame.locator("#xlv2-grid-input")
        # Add a delay of 100ms between key presses
        grid_input.press_sequentially(answer, delay=100)  

    def is_puzzle_filled(self) -> bool:
        filled = int(self.frame.locator("#xlv2-status-num-filled").text_content())
        total = int(self.frame.locator("#xlv2-status-num-total").text_content())
        return filled == total