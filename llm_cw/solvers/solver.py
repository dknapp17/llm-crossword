from abc import ABC, abstractmethod

from llm_cw.domain.crossword import ExolveAnswer, SolverClueInput, SolverConfig


class BaseSolver(ABC):

    @abstractmethod
    def solve_clue(
        self,
        clue: SolverClueInput,
        config: SolverConfig,

    ) -> ExolveAnswer:
        pass

    @abstractmethod
    def solve_puzzle(
        self,
        config: SolverConfig,

    ):
        pass


