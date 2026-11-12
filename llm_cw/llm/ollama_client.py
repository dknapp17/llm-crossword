import ollama


class OllamaClient:
    def __init__(self, model: str = "qwen3:4b"):
        self.model = model

    def generate(self, prompt: str) -> str:
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
        )

        return response["response"]