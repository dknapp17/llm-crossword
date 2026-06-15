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



    results = EmbeddedCrosswordDocument.vector_search(
        embedding=target_doc.clue_embedding,
        limit=6,
    )

    matches = []

    for result in results:

        if result["_id"] == str(target_doc.id):
            continue

        score = result["score"]

        matches.append((score, result))

    
    print(
            f"TARGET CLUE: "
            f"{target_doc.cleaned_clue_text} -> "
            f"{target_doc.cleaned_answer_text} | "
            f"{target_doc.id}"
        )

    print("TOP 5 SIMILAR")
    print("-" * 80)
    
    for score, doc in matches[:5]:

        print(
            f"CLUE: {doc['cleaned_clue_text']} "
            f"ANSWER: {doc['cleaned_answer_text']} "
            f"CLUE SIMILARITY SCORE: {doc['score']}"
        )


if __name__ == "__main__":
    main()