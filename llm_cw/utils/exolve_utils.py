from playwright.sync_api import Page

from llm_cw.domain.crossword import AcrossDown, SolverClueInput, SolverConfig
from llm_cw.utils.logging_utils import log_message


class ExolveController:
    def __init__(self, page: Page):
        self.page = page
        self.frame = page.frame_locator("#exolve-frame")

    def _read_streamlit_dropdown(self, label):
        dropdown = self.page.get_by_test_id("stSelectbox").filter(
            has=self.page.get_by_text(label, exact=True)
        )

        return dropdown.locator('[data-baseweb="select"]').inner_text()
    
    def get_solver_config(self) -> SolverConfig:
        model = self._read_streamlit_dropdown("Model")
        retrieval = self._read_streamlit_dropdown("Retrieval")
        solver_seed = 42
        return SolverConfig(model=model, retrieval=retrieval, solver_seed=solver_seed)

    def select_clue(self, direction: AcrossDown, number: int) -> None:
        clue = self.frame.locator(
            f'#xlv2-{direction.value} tr:has(> td.xlv-clue-label:text-is("{number}"))'
        )

        clue.click()

    def select_next_clue(self) -> None:
        self.frame.locator("#xlv2-next").click(delay=500)

    def _read_current_clue_id(self) -> tuple[int, AcrossDown]:
        label = self.frame.locator("#xlv2-curr-clue-label").inner_text()

        number = int(label.split("a")[0].split("d")[0])
        direction = (
            AcrossDown.ACROSS if "a" in label else AcrossDown.DOWN
        )

        return number, direction

    def is_current_clue_filled(self) -> bool:
        return self.frame.locator(
            "#xlv2-curr-clue-label"
        ).evaluate(
            "(element) => element.classList.contains('xlv-solved')"
        )
    
    def select_next_incomplete_clue(self) -> bool:
        while True:
            self.select_next_clue()
            is_solved = self.is_current_clue_filled()

            if not is_solved:
                return True
    
    def read_current_clue(self) -> SolverClueInput:
        number, direction = self._read_current_clue_id()
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
            number=number,
            direction=direction,
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