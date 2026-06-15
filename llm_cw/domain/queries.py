from pydantic import Field

from llm_cw.infrastructure.warehouse.mongo import NoSQLBaseDocument


class CrosswordQuery(NoSQLBaseDocument["CrosswordQuery"]):
    """
    A query object used for RAG over crossword clues.
    This represents a single retrieval unit (not a user query).
    """

    content: str

    # crossword-specific context
    answer_length: int | None = None
    clue_num: int | None = None
    across_down: str | None = None  # "across" | "down"

    # query expansion metadata
    expansion_type: str | None = None  # "base", "expanded", "length_hint", etc.

    metadata: dict = Field(default_factory=dict)

    class Settings:
        name = "crossword_queries"

    # -------------------------
    # helpers
    # -------------------------
    @classmethod
    def from_str(
        cls,
        query: str,
        *,
        answer_length: int | None = None,
        clue_num: int | None = None,
        across_down: str | None = None,
        expansion_type: str | None = None,
    ) -> "CrosswordQuery":
        return cls(
            content=query.strip(),
            answer_length=answer_length,
            clue_num=clue_num,
            across_down=across_down,
            expansion_type=expansion_type,
        )

    def with_content(self, new_content: str) -> "CrosswordQuery":
        return CrosswordQuery(
            id=self.id,
            content=new_content,
            answer_length=self.answer_length,
            clue_num=self.clue_num,
            across_down=self.across_down,
            expansion_type=self.expansion_type,
            metadata=self.metadata,
        )


class EmbeddedCrosswordQuery(CrosswordQuery):
    """
    Query with embedding for vector search.
    """

    embedding: list[float]

    class Settings:
        name = "crossword_queries"