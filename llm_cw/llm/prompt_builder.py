from llm_cw.domain.crossword import SolverClueInput


class PromptBuilder:
    def build(self, clue: SolverClueInput) -> str:
        known_letters = clue.positional_constraints or {}

        pattern = "".join(
            known_letters.get(i, "_")
            for i in range(clue.length)
        )

        return f"""
You are an expert crossword puzzle solver.

Solve the following crossword clue.

Clue: {clue.text}
Direction: {clue.direction}
Answer length: {clue.length}
Known letters: {pattern}

Instructions:
- Return a single answer matching the specified length.
- Respect all known letter constraints.
- Prefer common crossword answers.
- Return your best answer if multiple answers are possible.
"""