
import concurrent.futures

import llm_cw.domain.evaluation as eval
from llm_cw.rag.retriever import ContextRetriever

EVAL_PATH = "llm_cw/eval/eval_dataset.json"

def evaluate_example(ex, retriever):

    docs = retriever.search(
        query=ex.clue,
        k=1,
        expand_to_n_queries=1,
    )

    retrieved_ids = [d.id for d in docs]
    retrieval_rank = eval.rank_of(ex.document_id, retrieved_ids)

    reranked_docs = retriever.rerank(
        query=ex.clue,
        docs=docs,
        keep_top_k=5,
    )

    reranked_ids = [d.id for d in reranked_docs]
    rerank_rank = eval.rank_of(ex.document_id, reranked_ids)


    predicted_answer = (
        reranked_docs[0].cleaned_answer_text if reranked_docs else ""
    )

    return {
        "example_id": ex.document_id,
        "retrieved_ids": retrieved_ids,
        "reranked_ids": reranked_ids,
        "retrieval_rank": retrieval_rank,
        "rerank_rank": rerank_rank,
        "predicted_answer": predicted_answer,
        "correct_answer": ex.answer,
    }

def main():

    dataset = eval.load_eval_dataset(EVAL_PATH)
    retriever = ContextRetriever()

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(evaluate_example, ex, retriever)
            for ex in dataset
        ]

        results = [
            future.result()
            for future in concurrent.futures.as_completed(futures)
        ]
    metrics = eval.compute_metrics(results)

    print("\n" + "=" * 80)
    print("EVALUATION RESULTS")
    print("=" * 80)

    for k, v in metrics.items():
        print(f"{k:20s}: {v:.4f}")

    print("\nDone.")


if __name__ == "__main__":
    main()