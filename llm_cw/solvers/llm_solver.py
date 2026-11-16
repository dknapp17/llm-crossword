from llm_cw.domain.crossword import SolverAnswer, SolverClueInput, SolverConfig
from llm_cw.domain.response_schema import LLMAnswer
from llm_cw.domain.validator import BaseValidator
from llm_cw.llm.client import LLMClient
from llm_cw.llm.prompt_builder import PromptBuilder
from llm_cw.solvers.solver import BaseSolver


class LLMSolver(BaseSolver):
    def __init__(
            self, 
            config: SolverConfig, 
            validator: BaseValidator, 
            client: LLMClient
        ):
        super().__init__(config, validator)
        self.client = client
        self.validator = validator
        self.prompt_builder = PromptBuilder()

    def _generate_answer(self, clue: SolverClueInput) -> SolverAnswer:
        prompt = self.prompt_builder.build(clue)
        response = self.client.generate(prompt, LLMAnswer)

        return SolverAnswer(
            text=response.answer,
            length=clue.length,
            positional_text={i: letter for i, letter in enumerate(response.answer)},
            confidence=response.confidence,
        )