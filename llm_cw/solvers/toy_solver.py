from llm_cw.domain.crossword import ExolveAnswer, ExolveClue, SolverConfig
from llm_cw.solvers.solver import BaseSolver


class ToySolver(BaseSolver):
    def solve(
        self,
        clue: ExolveClue,
        config: SolverConfig,
    ) -> ExolveAnswer:
        """Used to demonstrate toy example of filling in X for every answer"""
        length = clue.answer_length
        toy_answer = "X" * length
        answer = ExolveAnswer.from_str(toy_answer)
        return answer