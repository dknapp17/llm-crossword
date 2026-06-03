#TODO: modify cleaning.py to take all docs from mongo and clean. 
# worry about storage in quadrant later

# query data warehouse
# clean documents
# load to vector db
from llm_cw.domain.documents import CrosswordDocument
from llm_cw.preprocessing.cleaning import clean_documents

raw_docs = CrosswordDocument.find()

clean_docs = clean_documents(raw_docs)
print(clean_docs[0])