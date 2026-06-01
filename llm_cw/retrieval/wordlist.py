from typing import Iterable


class WordList:
    def __init__(self, words: Iterable[str]):
        self._words = list(words)

    def all(self) -> list[str]:
        return self._words

    def by_length(self, length: int) -> list[str]:
        return [w for w in self._words if len(w) == length]