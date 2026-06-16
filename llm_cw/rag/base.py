from abc import ABC, abstractmethod
from typing import Any

from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel

from llm_cw.domain.queries import CrosswordQuery


class PromptTemplateFactory(ABC, BaseModel):
    @abstractmethod
    def create_template(self) -> PromptTemplate:
        pass


class RAGStep(ABC):
    def __init__(self, mock: bool = False) -> None:
        self._mock = mock

    @abstractmethod
    def generate(self, query: CrosswordQuery, *args, **kwargs) -> Any:
        pass