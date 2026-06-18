# this script should apply query expansion, retrieve multiple docs and rerank
# scripts/rag_demo.py

from llm_cw.rag.retriever import ContextRetriever


def main():

    clue = "Military position"

    retriever = ContextRetriever()

    print()
    print("=" * 80)
    print("QUERY")
    print("=" * 80)
    print(clue)

    results = retriever.search(
        query=clue,
        k=5,
        expand_to_n_queries=3,
    )

    print()
    print("=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)

    for idx, doc in enumerate(results, start=1):

        print()
        print(f"{idx}. {doc['clue_data']['text']}")
        print(f"   ANSWER: {doc['answer_data']['text']}")
        print(f"   ID: {doc['_id']}")


if __name__ == "__main__":
    main()