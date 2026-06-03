#TODO: modify cleaning.py to take all docs from mongo and clean. 
# worry about storage in quadrant later

# query data warehouse
# clean documents
# load to vector db
from llm_cw.domain.documents import CleanCrosswordDocument, CrosswordDocument
from llm_cw.preprocessing.cleaning import clean_documents

raw_docs = CrosswordDocument.find()

clean_docs = clean_documents(raw_docs)

CleanCrosswordDocument.bulk_insert(clean_docs)