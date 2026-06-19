# llm_cw/domain/evaluation.py

import json
from datetime import datetime

from pydantic import BaseModel


class EvaluationExample(BaseModel):
    clue: str
    answer: str
    answer_length: int
    puzzle_date: datetime
    document_id: str


class EvaluationPrediction(BaseModel):
    example_id: str

    retrieved_ids: list[str]
    reranked_ids: list[str]

    predicted_answer: str
    correct_answer: str

    retrieval_hit: bool
    rerank_hit: bool

    retrieval_rank: int | None
    rerank_rank: int | None

    confidence: float | None = None


class EvaluationMetrics(BaseModel):
    recall_at_3: float
    recall_at_5: float
    recall_at_10: float

    mrr: float

    rerank_mrr: float

    accuracy: float


class EvaluationRun(BaseModel):
    name: str
    timestamp: str

    metrics: EvaluationMetrics
    predictions: list[EvaluationPrediction]


def load_eval_dataset(path: str) -> list[EvaluationExample]:
    with open(path, "r") as f:
        raw = json.load(f)

    return [EvaluationExample(**item) for item in raw]


def rank_of(target_id: str, ids: list[str]) -> int | None:
    for i, _id in enumerate(ids):
        if _id == target_id:
            return i + 1
    return None


def compute_metrics(results: list[dict]) -> dict:

    def recall_at(k: int) -> float:
        return sum(
            1 for r in results
            if r["retrieval_rank"] is not None and r["retrieval_rank"] <= k
        ) / len(results)

    def mrr(key: str) -> float:
        total = 0.0
        for r in results:
            rank = r.get(key)
            total += (1 / rank) if rank else 0.0
        return total / len(results)

    accuracy = sum(
        1 for r in results
        if r["predicted_answer"].strip().lower()
        == r["correct_answer"].strip().lower()
    ) / len(results)

    return {
        "recall@3": recall_at(3),
        "recall@5": recall_at(5),
        "recall@10": recall_at(10),
        "retrieval_mrr": mrr("retrieval_rank"),
        "rerank_mrr": mrr("rerank_rank"),
        "accuracy": accuracy,
    }