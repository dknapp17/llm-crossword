from llm_cw.domain.response_schema import LLMAnswer
from llm_cw.domain.crossword import SolverClueInput, AcrossDown
from llm_cw.llm.prompt_builder import PromptBuilder
from llm_cw.llm.ollama_client import OllamaClient

client = OllamaClient()


clue = SolverClueInput(
    number=12,
    direction=AcrossDown.ACROSS,
    text="Feline pet",
    length=3,
    positional_constraints={0: "C", 2: "T"},
)

prompt = PromptBuilder().build(clue)
print(prompt)

response = client.generate(
    prompt=prompt,
    response_schema=LLMAnswer,
)

print(response)
print(response.answer)