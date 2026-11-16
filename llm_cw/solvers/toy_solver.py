import random

from llm_cw.domain.crossword import SolverAnswer, SolverClueInput
from llm_cw.solvers.solver import BaseSolver
from llm_cw.utils.logging_utils import log_message


class ToySolver(BaseSolver):
    def __init__(self, config, validator):
        super().__init__(config, validator)
        self.rng = random.Random(config.solver_seed)

    def _generate_answer(
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