from llm_cw.domain.documents import CleanCrosswordDocument, CrosswordDocument


def clean_text(text:str) -> str:
    return text

def clean_documents(
    documents: list[CrosswordDocument],
) -> list[CleanCrosswordDocument]:

    cleaned_docs = []

    for doc in documents:
        cleaned_docs.append(
            CleanCrosswordDocument(
                clue_data=doc.clue_data,
                answer_data=doc.answer_data,
                puzzle_data=doc.puzzle_data,
                cleaned_clue_text=clean_text(
                    doc.clue_data.text,
                ),
                cleaned_answer_text=clean_text(
                    doc.answer_data.text,
                ),
            )
        )

    return cleaned_docs
