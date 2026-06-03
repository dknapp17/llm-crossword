from llm_cw.domain.documents import CleanCrosswordDocument, CrosswordDocument
from llm_cw.preprocessing.cleaning import clean_documents

raw_docs = CrosswordDocument.find()

clean_docs = clean_documents(raw_docs)

CleanCrosswordDocument.bulk_insert(clean_docs)