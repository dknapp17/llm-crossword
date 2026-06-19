# llm_cw/domain/evaluation.py

from datetime import datetime

from pydantic import BaseModel


class EvaluationExample(BaseModel):
    clue: str
    answer: str
    answer_length: int
    puzzle_date: datetime
    document_id: str


class EvaluationPrediction(BaseModel):
    clue: str
    expected_answer: str
    predicted_answer: str
    confidence: float
    correct: bool


class EvaluationMetrics(BaseModel):
    recall_at_1: float
    recall_at_3: float
    recall_at_5: float
    accuracy: float