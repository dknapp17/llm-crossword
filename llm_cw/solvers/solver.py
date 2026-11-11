import random
from abc import ABC, abstractmethod

from llm_cw.domain.crossword import ExolveAnswer, SolverClueInput, SolverConfig


class BaseSolver(ABC):
    def __init__(self, config: SolverConfig):
        self.config = config
        self.rng = random.Random(config.solver_seed)

    @abstractmethod
    def solve_clue(
        self,
        clue: SolverClueInput,
    ) -> ExolveAnswer:
        pass

    @abstractmethod
    def solve_puzzle(self):
        pass


