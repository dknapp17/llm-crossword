from pydantic import BaseModel


class VectorSearchResult(BaseModel):
    id: str
    cleaned_clue_text: str
    cleaned_answer_text: str
    clue_embedding: list[float]
    score: float

    @classmethod
    def from_mongo(cls, doc: dict) -> "VectorSearchResult":
        return cls(
            id=str(doc["_id"]),
            cleaned_clue_text=doc["cleaned_clue_text"],
            cleaned_answer_text=doc["cleaned_answer_text"],
            clue_embedding=doc["clue_embedding"],
            score=doc["score"],
        )