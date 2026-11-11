from llm_cw.domain.crossword import SolverAnswer, SolverClueInput
from llm_cw.solvers.solver import BaseSolver
from llm_cw.utils.logging_utils import log_message


class ToySolver(BaseSolver):
    def solve_puzzle(self):
        """Used to demonstrate toy example of filling in X for every answer."""
        pass

    def solve_clue(
        self,
        clue: SolverClueInput,
    ) -> SolverAnswer:
        """Used to demonstrate toy example of filling in X for every answer."""
        log_message(
            f"Solving clue {clue.number} {clue.direction._value_}: {clue.text}"
        )
        length = clue.length
        answer = "X" * length
        confidence = self.rng.random()

        return SolverAnswer(
            text=answer,
            length=length,
            positional_text={i: letter for i, letter in enumerate(answer)},
            confidence=confidence,
        )