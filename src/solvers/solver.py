from abc import ABC, abstractmethod
from typing import List

from src.domain.crossword import CrosswordAnswer, CrosswordClue


class BaseSolver(ABC):

    @abstractmethod
    def solve(self, clue: CrosswordClue) -> List[CrosswordAnswer]:
        pass


