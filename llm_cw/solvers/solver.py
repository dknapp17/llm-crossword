from abc import ABC, abstractmethod

from llm_cw.domain.crossword import (
    SolverAnswer,
    SolverClueInput,
    SolverConfig,
)
from llm_cw.domain.validator import AnswerValidator


class BaseSolver(ABC):

    def __init__(
        self,
        config: SolverConfig,
        validator: AnswerValidator,
    ):
        self.config = config
        self.validator = validator

    def solve_clue(
        self,
        clue: SolverClueInput,
    ) -> SolverAnswer:

        answer = self._generate_answer(clue)

        is_valid = self.validator.validate(clue, answer)

        answer.text = '' * clue.length if not is_valid else answer.text

        return answer

    @abstractmethod
    def _generate_answer(
        self,
        clue: SolverClueInput,
    ) -> SolverAnswer:
        pass


