from llm_cw.domain.crossword import SolverClueInput, SolverConfig
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
    ) -> str:
        """Used to demonstrate toy example of filling in X for every answer"""
        length = clue.length
        answer = "X" * length
        return answer