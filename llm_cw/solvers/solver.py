from abc import ABC, abstractmethod

from llm_cw.domain.crossword import ExolveAnswer, ExolveClue, SolverConfig


class BaseSolver(ABC):

    @abstractmethod
    def solve(
        self,
        clue: ExolveClue,
        config: SolverConfig,

    ) -> ExolveAnswer:
        pass


