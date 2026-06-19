import json

from llm_cw.domain.documents import EmbeddedCrosswordDocument
from llm_cw.domain.evaluation import EvaluationExample

TEST_SIZE = 0.2  # still used, but now applied on time axis


def parse_date(doc):
    """
    Safely extract puzzle date for sorting.
    Adjust this if your schema differs (string vs datetime).
    """
    return doc.puzzle_data.puzzle_date


def main():

    docs = EmbeddedCrosswordDocument.find()

    # 1. Filter out docs without dates (safety)
    docs = [d for d in docs if d.puzzle_data and d.puzzle_data.puzzle_date]

    # 2. Sort chronologically (CRITICAL for temporal split)
    docs.sort(key=parse_date)

    # 3. Time-based split point
    split_idx = int(len(docs) * (1 - TEST_SIZE))

    train_docs = docs[:split_idx]
    test_docs = docs[split_idx:]

    print(f"Total docs: {len(docs)}")
    print(f"Train: {len(train_docs)}")
    print(f"Test: {len(test_docs)}")

    # 4. Build evaluation examples ONLY from test (future/unseen data)
    examples = [
        EvaluationExample(
            clue=doc.cleaned_clue_text,
            answer=doc.answer_data.text,
            answer_length=doc.clue_data.length,
            puzzle_date=doc.puzzle_data.puzzle_date,
            document_id=str(doc.id),
        )
        for doc in test_docs
    ]

    # sanity check
    print("\nSample evaluation example:\n")
    print(examples[0])

    # 5. Save dataset
    output_path = "llm_cw/eval/eval_dataset.json"

    with open(output_path, "w") as f:
        json.dump(
            [e.model_dump() for e in examples],
            f,
            indent=2,
            default=str,  # handles datetime if present
        )

    print(f"\nSaved eval dataset to {output_path}")


if __name__ == "__main__":
    main()