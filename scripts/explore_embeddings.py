# scripts/explore_embedding.py

import sys

import numpy as np

from llm_cw.domain.documents import EmbeddedCrosswordDocument


def cosine_similarity(a: list[float], b: list[float]) -> float:
    a = np.array(a)
    b = np.array(b)

    return float(
        np.dot(a, b)
        / (np.linalg.norm(a) * np.linalg.norm(b))
    )


def main():

    if len(sys.argv) != 2:
        raise ValueError(
            "Usage: python scripts/explore_embedding.py <uuid>"
        )

    doc_id = sys.argv[1]

    target_doc = EmbeddedCrosswordDocument.get_by_id(doc_id=doc_id)

    if not target_doc:
        raise ValueError(f"Document not found: {doc_id}")

    all_docs = EmbeddedCrosswordDocument.find()

    results = []

    for doc in all_docs:

        if doc.id == target_doc.id:
            continue

        similarity = cosine_similarity(
            target_doc.clue_embedding,
            doc.clue_embedding,
        )

        results.append((similarity, doc))

    results.sort(
        key=lambda x: x[0],
        reverse=True,
    )

    print()
    print("TARGET")
    print("-" * 80)
    print(target_doc.cleaned_clue_text)
    print(f"ANSWER: {target_doc.cleaned_answer_text}")
    print()

    print("TOP 5 SIMILAR")
    print("-" * 80)

    for similarity, doc in results[:5]:
        print(
            f"{similarity:.4f} | "
            f"{doc.cleaned_clue_text} -> "
            f"{doc.cleaned_answer_text} | "
            f"{doc.id}"
        )


if __name__ == "__main__":
    main()