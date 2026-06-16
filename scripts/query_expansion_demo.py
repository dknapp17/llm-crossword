# scripts/query_expansion_demo.py

from llm_cw.domain.documents import EmbeddedCrosswordDocument
from llm_cw.domain.queries import CrosswordQuery
from llm_cw.preprocessing.embedding import embed_queries
from llm_cw.rag.query_expansion import QueryExpansion

#TODO: add embedding to expander

def main():

    query = CrosswordQuery.from_str(
        "Military position",
        answer_length=8,
    )

    expander = QueryExpansion()

    expanded_queries = expander.generate(
        query=query,
        expand_to_n=5,
    )

    embedded_queries = embed_queries(expanded_queries)

    print()
    print("ORIGINAL QUERY")
    print("-" * 80)
    print(query.content)

    print()
    print("EXPANDED QUERIES")
    print("-" * 80)

    for i, embedded_query in enumerate(embedded_queries, start=1):
        print(f"{i}. {embedded_query.content}")

        results = EmbeddedCrosswordDocument.vector_search(
            embedding=embedded_query.embedding,
            limit=3
        )
        matches = []
        for result in results:

            score = result["score"]

            matches.append((score, result))

        print("TOP 3 SIMILAR CLUES")
        
        for score, doc in matches[:3]:

            print(
                f"CLUE: {doc['cleaned_clue_text']} | "
                f"ANSWER: {doc['cleaned_answer_text']} | "
                f"CLUE SIMILARITY SCORE: {doc['score']}"
            )
        print("_" * 80)


if __name__ == "__main__":
    main()