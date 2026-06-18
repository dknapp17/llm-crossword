import concurrent.futures

from llm_cw.domain.documents import EmbeddedCrosswordDocument
from llm_cw.domain.queries import CrosswordQuery, EmbeddedCrosswordQuery
from llm_cw.domain.search import VectorSearchResult
from llm_cw.preprocessing.embedding import embed_query
from llm_cw.rag.query_expansion import QueryExpansion
from llm_cw.rag.reranker import Reranker


class ContextRetriever:
    def __init__(self, mock: bool = False) -> None:
        self._query_expander = QueryExpansion()
        self._reranker = Reranker()

    def search(
        self,
        query: str,
        k: int = 3,
        expand_to_n_queries: int = 3,
    ) -> list[VectorSearchResult]:

        query_model = CrosswordQuery.from_str(query)

        n_generated_queries = self._query_expander.generate(
            query_model,
            expand_to_n=expand_to_n_queries,
        )

        with concurrent.futures.ThreadPoolExecutor() as executor:

            search_tasks = [
                executor.submit(
                    self._search,
                    _query_model,
                    k,
                )
                for _query_model in n_generated_queries
            ]

            n_k_documents = []

            for task in concurrent.futures.as_completed(search_tasks):
                n_k_documents.extend(task.result())

        # dedupe by mongo _id
        #TODO: put this in a function
        seen = set()
        deduped = []

        for doc in n_k_documents:
            if doc.id in seen:
                continue
            seen.add(doc.id)
            deduped.append(doc)

        n_k_documents = deduped
        # unique_docs = {}

        # for doc in n_k_documents:
        #     unique_docs[str(doc["_id"])] = doc

        # n_k_documents = list(unique_docs.values())

        # if len(n_k_documents) > 0:
        #     k_documents = self.rerank(
        #         query=query_model,
        #         docs=n_k_documents,
        #         keep_top_k=k,
        #     )
        # else:
        #     k_documents = []

        return n_k_documents

    def _search(
        self,
        query: CrosswordQuery,
        k: int = 3
    ) -> list[VectorSearchResult]:
        assert k >= 3, "k should be >= 3"

        embedded_query: EmbeddedCrosswordQuery = embed_query(query)

        raw_results = EmbeddedCrosswordDocument.vector_search(
            embedding=embedded_query.embedding,
            limit=k
        )

        results: list[VectorSearchResult] = [
            VectorSearchResult.from_mongo(doc)
            for doc in raw_results
        ]

        return results
    
    
    def rerank(self,
               query: str | CrosswordQuery, 
               docs: list[VectorSearchResult], 
               keep_top_k: int=3
        ) -> list[VectorSearchResult]:
        
        if isinstance(query, str):
            query = CrosswordQuery.from_str(query)

        reranked_documents = self._reranker.generate(query=query, 
                                                     docs=docs, 
                                                     keep_top_k=keep_top_k
        )

        return reranked_documents