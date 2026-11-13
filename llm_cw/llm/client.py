from typing import Protocol

from pydantic import BaseModel


class LLMClient(Protocol):
    def generate(
        self,
        prompt: str,
        response_schema: type[BaseModel],
    ) -> BaseModel:
        ...