from transformers import pipeline

from llm_cw.domain.queries import CrosswordQuery
from llm_cw.settings import settings

from .base import RAGStep
from .prompt_templates import QueryExpansionTemplate


class QueryExpansion(RAGStep):

    def __init__(self):
        super().__init__()

        self.generator = pipeline(
            "text-generation",
            model=settings.HF_MODEL_ID,
            device_map="auto",
        )

    def generate(
        self,
        query: CrosswordQuery,
        expand_to_n: int,
    ) -> list[CrosswordQuery]:

        assert expand_to_n > 0, (
            f"'expand_to_n' should be > 0. Got {expand_to_n}."
        )

        if self._mock:
            return [query for _ in range(expand_to_n)]

        query_expansion_template = QueryExpansionTemplate()

        prompt = query_expansion_template.create_template(
            expand_to_n - 1
        ).format(
            question=query.content,
        )

        response = self.generator(
            prompt,
            max_new_tokens=200,
            do_sample=False,
        )

        result = response[0]["generated_text"]

        result = result[len(prompt):]

        queries_content = result.strip().split(
            query_expansion_template.separator
        )

        queries = [query]

        queries += [
            query.with_content(stripped_content)
            for content in queries_content
            if (stripped_content := content.strip())
        ]

        return queries