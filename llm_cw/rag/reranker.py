from llm_cw.domain.documents import EmbeddedCrosswordDocument
from llm_cw.domain.queries import CrosswordQuery
from llm_cw.preprocessing.embedding import CrossEncoderModelSingleton

from .base import RAGStep


class Reranker(RAGStep):
    def __init__(self, mock: bool = False) -> None:
        super().__init__(mock=mock)

        self._model = CrossEncoderModelSingleton()

    def generate(self, query: CrosswordQuery, 
                 docs: list[EmbeddedCrosswordDocument], 
                 keep_top_k: int) -> list[EmbeddedCrosswordDocument]:
        if self._mock:
            return docs

        query_doc_tuples = [(query.content, doc['clue_data']['text']) for doc in docs]
        scores = self._model(query_doc_tuples)

        scored_query_doc_tuples = list(zip(scores, docs, strict=False))
        scored_query_doc_tuples.sort(key=lambda x: x[0], reverse=True)

        reranked_documents = scored_query_doc_tuples[:keep_top_k]
        reranked_documents = [doc for _, doc in reranked_documents]

        return reranked_documents