from dataclasses import dataclass
from datetime import datetime
from enum import Enum


# utility objects
class AcrossDown(str, Enum):
    ACROSS = "across"
    DOWN = "down"


# crossword objects
@dataclass
class CrosswordClue:
    text: str
    across_down: AcrossDown
    clue_num: int

@dataclass
class ExolveClue:
    index: str
    clue_text: str
    answer_length: int
    positional_constraints: dict[int, str]  # ex: {0: C} for C _ _

@dataclass
class ExolveAnswer:
    answer_text: str
    answer_length: int
    positional_text: dict[int, str]  # ex: {0: C} for C _ _

    @classmethod
    def from_str(cls, text: str) -> "ExolveAnswer":
        text = text.upper()

        return cls(
            answer_text=text,
            answer_length=len(text),
            positional_text={
                i: letter for i, letter in enumerate(text)
            },
        )

    @classmethod
    def from_dict(cls, positional_text: dict[int, str]) -> "ExolveAnswer":
        positional_text = {
            int(i): letter.upper()
            for i, letter in positional_text.items()
        }

        answer_text = "".join(
            positional_text[i] for i in sorted(positional_text)
        )

        return cls(
            answer_text=answer_text,
            answer_length=len(answer_text),
            positional_text=positional_text,
        )

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

# Solver objects
@dataclass
class SolverConfig:
    model: str  # ex: "Default"
    retrieval: str  # ex: "RAG"

@dataclass
class SolverClueInput:
    text: str  # ex: Feline
    length: int  # ex: 3
    positional_constraints: dict[int, str]  # ex: {0: C} for C _ _


@dataclass
class SolverAnswer:
    text: str  # ex: DEADHEAT
    length: int
    positional_text: dict[int, str]  # ex: {0: D, 1: E, 2: A, 3: D}


# Grid objects

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