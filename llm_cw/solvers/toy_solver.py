import random

from llm_cw.domain.crossword import SolverAnswer, SolverClueInput, SolverConfig
from llm_cw.solvers.solver import BaseSolver


class ToySolver(BaseSolver):
    def solve_puzzle(self, config: SolverConfig):
        """Used to demonstrate toy example of filling in X for every answer"""
        # This method can be implemented to solve the entire puzzle if needed
        pass
    
    def solve_clue(
        self,
        clue: SolverClueInput,
        config: SolverConfig,
    ) -> SolverAnswer:
        """Used to demonstrate toy example of filling in X for every answer"""
        length = clue.length
        answer = "X" * length
        random.seed(config.solver_seed)
        confidence = random.random()

        return SolverAnswer(
            text=answer,
            length=length,
            positional_text={i: letter for i, letter in enumerate(answer)},
            confidence=confidence
        )