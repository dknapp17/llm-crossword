from llm_cw.domain.crossword import AcrossDown
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

class CrosswordClueAnswerPairDocument(NoSQLBaseDocument["CrosswordClueAnswerPairDocument"]):
    length: int
    clue_text: str
    answer_text: str
    positional_text: dict

    # optional future ML fields
    source_url: str | None = None
    puzzle_date: str | None = None

    class Settings:
        name = "cw_clue_answer"