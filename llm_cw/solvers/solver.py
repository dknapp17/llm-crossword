import random
from abc import ABC, abstractmethod

from llm_cw.domain.crossword import SolverAnswer, SolverClueInput, SolverConfig


class BaseSolver(ABC):
    def __init__(self, config: SolverConfig):
        self.config = config
        self.rng = random.Random(config.solver_seed)

    @abstractmethod
    def solve_clue(
        self,
        clue: SolverClueInput,
    ) -> SolverAnswer:
        pass

    @abstractmethod
    def solve_puzzle(self):
        pass


