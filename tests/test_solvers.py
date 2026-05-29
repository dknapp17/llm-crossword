import unittest

from src.domain.crossword import CrosswordAnswer, SolverClueInput
from src.retrieval.wordlist import WordList
from src.solvers.algorithmic_solver import AlgorithmicSolver


class TestAlgorithmicSolver(unittest.TestCase):

    def setUp(self):
        # tiny deterministic wordlist for tests
        words = [
            "cat",
            "car",
            "cap",
            "dog",
            "dot",
            "cow",
        ]

        self.wordlist = WordList(words)
        self.solver = AlgorithmicSolver(self.wordlist)

    def test_filters_by_length(self):
        clue = SolverClueInput(
            text="feline",
            length=3,
            weekday_num=1,
            positional_constraints=None
        )

        results = self.solver.solve(clue)

        self.assertTrue(all(len(r.text) == 3 for r in results))

    def test_filters_by_constraints(self):
        clue = SolverClueInput(
            text="vehicle",
            length=3,
            weekday_num=1,
            positional_constraints={0: "c"}  # must start with 'c'
        )

        results = self.solver.solve(clue)

        self.assertTrue(all(r.text.lower().startswith("c") for r in results))

    def test_returns_crossword_answers(self):
        clue = SolverClueInput(
            text="animal",
            length=3,
            weekday_num=1,
            positional_constraints=None
        )

        results = self.solver.solve(clue)

        self.assertTrue(all(isinstance(r, CrosswordAnswer) for r in results))

    def test_empty_result_when_no_match(self):
        clue = SolverClueInput(
            text="impossible",
            length=3,
            weekday_num=1,
            positional_constraints={0: "z"}  # no word starts with z in list
        )

        results = self.solver.solve(clue)

        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()