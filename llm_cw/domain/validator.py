from abc import ABC, abstractmethod

import spacy

from llm_cw.domain.crossword import SolverAnswer, SolverClueInput
from llm_cw.utils.logging_utils import log_message

nlp = spacy.load("en_core_web_sm")

# utility functions

def _validate_positional_constraints(
            answer_text: str,
            positional_constraints: dict[int: str]) -> bool:
        
        answer = answer_text.upper()

        for position, expected_char in positional_constraints.items():
            if position < 0 or position >= len(answer):
                return False

            if answer[position] != expected_char.upper():
                return False

        return True

def _validate_grammatical_number(clue_text: str, answer_text: str) -> bool:
    clue_doc = nlp(clue_text)
    answer_doc = nlp(answer_text)

    clue_root = next(
        (
            token
            for token in clue_doc
            if token.pos_ == "NOUN" and token.dep_ == "ROOT"
        ),
        None,
    )

    answer_root = next(
        (
            token
            for token in answer_doc
            if token.pos_ == "NOUN" and token.dep_ == "ROOT"
        ),
        None,
    )

    if clue_root is None:
        return True

    if answer_root is None:
        return False

    clue_number = clue_root.morph.get("Number")
    answer_number = answer_root.morph.get("Number")

    return clue_number == answer_number
        
# validator objects

class BaseValidator(ABC):
    @abstractmethod
    def validate(
        self,
    ) -> bool:
        pass


class AnswerLengthValidator(BaseValidator):
    def validate(
        self,
        clue: SolverClueInput,
        answer: SolverAnswer,
    ) -> bool:

        if len(answer.text) != clue.length:
            return False

        return True


class PositionalConstraintValidator(BaseValidator):
    def validate(
        self,
        clue: SolverClueInput,
        answer: SolverAnswer,
    ) -> bool:

        return _validate_positional_constraints(
            answer.text,
            clue.positional_constraints
        )

class GrammaticalNumberValidator(BaseValidator):
    def validate(
        self,
        clue: SolverClueInput,
        answer: SolverAnswer,
    ) -> bool:

        return _validate_grammatical_number(
            clue.text,
            answer.text
        )

class AnswerValidator:
    def __init__(self, validators: list[BaseValidator]):
        self.validators = validators

    def validate(
        self,
        clue: SolverClueInput,
        answer: SolverAnswer,
    ) -> bool:

        # TODO make errors useful
        error_count = 0

        for validator in self.validators:
            is_valid = validator.validate(clue, answer)

            if not is_valid:
                error_count += 1
                log_message(
                    f"{validator.__class__.__name__} failed validation "
                    f"for clue '{clue.text}' with answer '{answer.text}'"
                )

        return error_count == 0
