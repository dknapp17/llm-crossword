from functools import cached_property

from sentence_transformers import SentenceTransformer

from llm_cw.domain.documents import CleanCrosswordDocument, EmbeddedCrosswordDocument
from llm_cw.domain.queries import CrosswordQuery, EmbeddedCrosswordQuery
from llm_cw.settings import settings


class EmbeddingModelSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance._model = SentenceTransformer(
                settings.EMBEDDING_MODEL_ID,
                device=settings.EMBEDDING_DEVICE,
            )

            cls._instance._model.eval()

        return cls._instance

    @property
    def model_id(self) -> str:
        return self._model._model_card_vars.get(
            "model_name",
            settings.EMBEDDING_MODEL_ID,
        )

    @cached_property
    def embedding_size(self) -> int:
        return len(self._model.encode(""))

    def __call__(
        self,
        text: str | list[str],
    ) -> list[float] | list[list[float]]:
        embeddings = self._model.encode(text)

        return embeddings.tolist()


embedding_model = EmbeddingModelSingleton()

def embed_text(text:str) -> str:
    return embedding_model(text)

def embed_texts(texts: list[str]) -> list[list[float]]:
    return embedding_model(texts)

def embed_documents(
    documents: list[CleanCrosswordDocument],
) -> list[EmbeddedCrosswordDocument]:

    embedded_docs = []

    for doc in documents:
        embedded_docs.append(
            EmbeddedCrosswordDocument(
                clue_data=doc.clue_data,
                answer_data=doc.answer_data,
                puzzle_data=doc.puzzle_data,
                cleaned_clue_text=doc.cleaned_clue_text,
                cleaned_answer_text=doc.cleaned_answer_text,
                is_clean=doc.is_clean,
                clue_embedding=embed_text(doc.cleaned_clue_text),
                answer_embedding=embed_text(doc.cleaned_answer_text)
            )
        )

    return embedded_docs

def embed_query(query: CrosswordQuery) -> EmbeddedCrosswordQuery:


    embedded_query = EmbeddedCrosswordQuery(
        content=query.content,
        embedding=embed_text(query.content)
    )

    return embedded_query

def embed_queries(
    queries: list[CrosswordQuery],
) -> list[EmbeddedCrosswordQuery]:

    embedded_queries = []

    for query in queries:
        embedded_queries.append(
            EmbeddedCrosswordQuery(
                content=query.content,
                embedding=embed_text(query.content)
            )
        )

    return embedded_queries