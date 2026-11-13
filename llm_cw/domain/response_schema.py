from pydantic import BaseModel, Field


class LLMAnswer(BaseModel):
    answer: str = Field(description="The proposed crossword answer")
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="The model's self-reported confidence in its answer",
    )
    # explanation: str = Field(
    #     description="A brief explanation of why the answer fits the clue"
    # )