import concurrent.futures

from llm_cw.domain.documents import EmbeddedCrosswordDocument
from llm_cw.domain.queries import CrosswordQuery, EmbeddedCrosswordQuery
from llm_cw.preprocessing.embedding import embed_query
from llm_cw.rag import QueryExpansion
from llm_cw.utils import cw_utils

# from .reranking import Reranker


class ContextRetriever:
    def __init__(self, mock: bool = False) -> None:
        self._query_expander = QueryExpansion(mock=mock)
        # self._reranker = Reranker(mock=mock)

    def search(
        self,
        query: str,
        k: int = 3,
        expand_to_n_queries: int = 3,
    ) -> list:
        query_model = CrosswordQuery.from_str(query)

        n_generated_queries = self._query_expander.generate(
            query_model, 
            expand_to_n=expand_to_n_queries
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
            n_k_documents = [
                task.result() 
                for task in concurrent.futures.as_completed(search_tasks)
            ]
            n_k_documents = cw_utils.flatten(n_k_documents)
            n_k_documents = list(set(n_k_documents))


        if len(n_k_documents) > 0:
            k_documents = self.rerank()
        else:
            k_documents = []

        return k_documents

    def _search(
            self, 
            query: CrosswordQuery,
              k: int = 3
        ) -> list[EmbeddedCrosswordDocument]:
        assert k >= 3, "k should be >= 3"

        # TODO: add filtering
        # query_filter = None

        embedded_query: EmbeddedCrosswordQuery = embed_query(query)

        retrieved_docs = EmbeddedCrosswordDocument.vector_search(
            embedding=embedded_query.embedding,
            limit=3
        )
        # retrieved_chunks = post_chunks + articles_chunks + repositories_chunks

        return retrieved_docs
    
    def rerank(self, n_k_documents: list):
        return n_k_documents

    # def rerank(self, 
    # query: str | Query, chunks: list[EmbeddedChunk], 
    # keep_top_k: int) -> list[EmbeddedChunk]:
    #     if isinstance(query, str):
    #         query = Query.from_str(query)

    #     reranked_documents = self._reranker.generate(query=query, 
    # chunks=chunks, 
    # keep_top_k=keep_top_k)

    #     logger.info(f"{len(reranked_documents)} documents reranked successfully.")

    #     return reranked_documents