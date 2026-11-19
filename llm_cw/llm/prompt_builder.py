from llm_cw.domain.crossword import SolverClueInput
from llm_cw.domain.search import VectorSearchResult


class PromptBuilder:
    def build(
        self,
        clue: SolverClueInput,
        context: list[VectorSearchResult] | None = None,
    ) -> str:
        known_letters = clue.positional_constraints or {}

        pattern = "".join(
            known_letters.get(i, "_")
            for i in range(clue.length)
        )

        prompt = f"""
You are an expert crossword puzzle solver.

Solve the following crossword clue.

Clue: {clue.text}
Direction: {clue.direction}
Answer length: {clue.length}
Known letters: {pattern}
"""

        if context:
            examples = "\n".join(
                f"- Clue: {doc.clue}\n  Answer: {doc.answer}"
                for doc in context
            )

            prompt += f"""
Similar historical crossword clues and their answers:

{examples}

Use these examples as reference material when solving the current clue.
They may provide useful synonyms, definitions, or related meanings.
Do not blindly copy an answer; determine which answer best fits the
current clue.
"""

        prompt += """
Instructions:
- Return a single answer matching the specified length.
- Respect all known letter constraints.
- Prefer common crossword answers.
- Return your best answer if multiple answers are possible.
"""

        return prompt