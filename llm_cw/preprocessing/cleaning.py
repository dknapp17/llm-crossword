from llm_cw.domain.documents import CleanCrosswordDocument, CrosswordDocument


def clean_text() -> str:
    pass

def clean_documents(
        documents: list[CrosswordDocument]
):
    cleaned_documents = []
    for document in documents:
        cleaned_documents.append(
            CleanCrosswordDocument(
                id = ''
            )
        )
    return documents
