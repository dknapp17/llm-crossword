# scripts/query_expansion_demo.py

from pprint import pprint

from llm_cw.domain.queries import CrosswordQuery
from llm_cw.rag.query_expansion import QueryExpansion


def main():

    query = CrosswordQuery.from_str(
        "Fine Fodder for a Freudian analyst",
        answer_length=8,
        clue_num=12,
        across_down="across",
    )

    expander = QueryExpansion()

    expanded_queries = expander.generate(
        query=query,
        expand_to_n=5,
    )

    print()
    print("ORIGINAL QUERY")
    print("-" * 80)
    print(query.content)

    print()
    print("EXPANDED QUERIES")
    print("-" * 80)

    for i, expanded_query in enumerate(expanded_queries, start=1):
        print(f"{i}. {expanded_query.content}")

    print()
    print("FULL OBJECTS")
    print("-" * 80)

    for query in expanded_queries:
        pprint(query.model_dump())
        print()


if __name__ == "__main__":
    main()