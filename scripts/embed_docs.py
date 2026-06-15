from llm_cw.domain.documents import CleanCrosswordDocument, EmbeddedCrosswordDocument
from llm_cw.preprocessing.embedding import embed_documents

clean_docs = CleanCrosswordDocument.find()

embedded_docs = embed_documents(clean_docs)

EmbeddedCrosswordDocument.bulk_insert(embedded_docs)