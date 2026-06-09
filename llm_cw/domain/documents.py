from llm_cw.domain.crossword import (
    AcrossDown,
    CrosswordPuzzleData,
    SolverAnswer,
    SolverClueInput,
)
from llm_cw.infrastructure.warehouse.mongo import NoSQLBaseDocument


class CrosswordClueDocument(NoSQLBaseDocument["CrosswordClueDocument"]):
    text: str
    across_down: AcrossDown
    clue_num: int

    class Settings:
        name = "crossword_clues"

class CrosswordAnswerDocument(NoSQLBaseDocument["CrosswordAnswerDocument"]):
    text: str
    across_down: AcrossDown
    clue_num: int

    class Settings:
        name = "crossword_answers"

class CrosswordDocument(
    NoSQLBaseDocument["CrosswordDocument"]
):
    clue_data: SolverClueInput
    answer_data: SolverAnswer
    puzzle_data: CrosswordPuzzleData

    class Settings:
        name = "cw_clue_answer"

class CleanCrosswordDocument(CrosswordDocument):
    cleaned_clue_text: str
    cleaned_answer_text: str

    is_clean: bool=True

    class Settings:
        name = "cw_clean"

class EmbeddedCrosswordDocument(CleanCrosswordDocument):
    clue_embedding: list[float] | None
    answer_embedding: list[float] | None
    
    class Settings:
        name = "cw_embedded"