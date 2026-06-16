from langchain_core.prompts import PromptTemplate

from .base import PromptTemplateFactory


class QueryExpansionTemplate(PromptTemplateFactory):
    prompt: str = """You are an AI language model assistant trained to solve crosswords.
    Your task is to generate {expand_to_n} different versions of the given clue to 
    retrieve relevant documents from a vector database. By generating multiple 
    perspectives on the clue, you can uncover multiple meanings and detect wordplay. 
    Keep alternatives short and concise.

    Return ONLY the rewritten queries.
        - One query per line
        - No numbering
        - No explanations
        - No bullets
        - No extra text

        Example output:
        Military rank highest authority
        Supreme command military rank
        Top level military position
        Highest military grade
    Provide these alternative clues seperated by '{separator}'.
    Original question: {question}"""

    @property
    def separator(self) -> str:
        return "#next-question#"

    def create_template(self, expand_to_n: int) -> PromptTemplate:
        return PromptTemplate(
            template=self.prompt,
            input_variables=["question"],
            partial_variables={
                "separator": self.separator,
                "expand_to_n": expand_to_n,
            },
        )