from abc import ABC, abstractmethod

from llm_cw.domain.crossword import SolverAnswer, SolverClueInput
from llm_cw.utils.logging_utils import log_message

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
            log_message(
                f"Answer {answer.text} does not match expected length for clue "
                f"{clue.number, clue.direction._value_}"
            )
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

        return error_count == 0
