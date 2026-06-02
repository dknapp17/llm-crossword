from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AcrossDown(str, Enum):
    ACROSS = "across"
    DOWN = "down"

@dataclass
class CrosswordClue:
    text: str
    across_down: AcrossDown
    clue_num: int

@dataclass
class CrosswordAnswer:
    text: str
    across_down: AcrossDown
    clue_num: int

@dataclass
class CrosswordClueAnswerPair:
    crossword_clue: CrosswordClue
    crossword_answer: CrosswordAnswer

@dataclass 
class CrosswordPuzzleData:
    puzzle_date: datetime
    puzzle_dow: int
    puzzle_url: str

@dataclass
class SolverClueInput:
    text: str  # ex: Feline
    length: int  # ex: 3
    positional_constraints: dict[int, str]  # ex: {1: C} for C _ _


@dataclass
class SolverAnswer:
    text: str  # ex: DEADHEAT
    length: int
    positional_text: dict[str, str]  # ex: {1: DH, 2: E, 3: A, 4: DT}

@dataclass
class CrosswordGridSquare:
    row: int
    col: int
    isblack: bool
    solution_text: str | None = None
    clue_num: int | None = None


@dataclass
class CrosswordGrid:
    squares: list[list[CrosswordGridSquare]]

    def __post_init__(self):
        self._by_clue_num: dict[int, CrosswordGridSquare] = {}

        for row in self.squares:
            for sq in row:
                if sq.clue_num is not None:
                    self._by_clue_num[sq.clue_num] = sq

    @property
    def rows(self) -> int:
        return len(self.squares)

    @property
    def cols(self) -> int:
        return len(self.squares[0]) if self.squares else 0

    def get(self, row: int, col: int) -> CrosswordGridSquare:
        return self.squares[row][col]

    def get_by_clue_num(self, clue_num: int) -> CrosswordGridSquare:
        return self._by_clue_num.get(clue_num,"")