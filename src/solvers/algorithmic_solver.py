from src.domain.crossword import CrosswordAnswer, CrosswordClue
from src.solvers.solver import BaseSolver


class AlgorithmicSolver(BaseSolver):

    def __init__(self, wordlist: list[str]):
        self.wordlist = wordlist

    def _matches_constraints(self, 
                             word: str, 
                             constraints: dict[int, str] | None) -> bool:
        if not constraints:
            return True

        for idx, letter in constraints.items():
            if idx >= len(word) or word[idx].lower() != letter.lower():
                return False
        return True

    def solve(self, clue: CrosswordClue) -> list[CrosswordAnswer]:

        candidates = []

        for word in self.wordlist:
            if len(word) != clue.length:
                continue

            if not self._matches_constraints(word, clue.positional_constraints):
                continue

            candidates.append(
                CrosswordAnswer(
                    text=word.upper(),
                    length=len(word),
                    positional_text={}
                )
            )

        return candidates[:10]