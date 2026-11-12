import ollama
from pydantic import BaseModel


class OllamaClient:
    def __init__(self, model: str = "qwen3:4b"):
        self.model = model

    def generate(
        self,
        prompt: str,
        response_schema: type[BaseModel],
    ) -> BaseModel:
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            format=response_schema.model_json_schema(),
            think=False
        )

        return response_schema.model_validate_json(response["response"])