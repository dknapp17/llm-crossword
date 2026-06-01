from abc import ABC, abstractmethod
from typing import List

from llm_cw.domain.crossword import CrosswordAnswer, CrosswordClue


class BaseSolver(ABC):

    @abstractmethod
    def solve(self, clue: CrosswordClue) -> List[CrosswordAnswer]:
        pass


