from src.domain.crossword import SolverAnswer, SolverClueInput
from src.retrieval.wordlist import WordList
from src.solvers.solver import BaseSolver


class AlgorithmicSolver(BaseSolver):

    def __init__(self, wordlist: WordList):
        self.wordlist = wordlist

    def solve(self, clue: SolverClueInput) -> list[SolverAnswer]:

        words = self.wordlist.by_length(clue.length)
        words = self._filter_by_constraints(words, clue.positional_constraints)

        return self._to_answers(words)

    def _filter_by_constraints(
        self,
        words: list[str],
        constraints: dict[int, str] | None
    ) -> list[str]:

        if not constraints:
            return words

        result = []
        for word in words:
            if all(
                idx < len(word) and word[idx].lower() == letter.lower()
                for idx, letter in constraints.items()
            ):
                result.append(word)

        return result

    def _to_answers(self, words: list[str]) -> list[SolverAnswer]:
        return [
            SolverAnswer(
                text=w.upper(),
                length=len(w),
                positional_text={}
            )
            for w in words
        ]