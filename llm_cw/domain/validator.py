from abc import ABC, abstractmethod

from llm_cw.domain.crossword import SolverAnswer, SolverClueInput
from llm_cw.utils.logging_utils import log_message


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
                f'Answer {answer.text} does not match expected length for clue '
                f'{clue.number, clue.direction._value_}'
            )
            return False

        return True

class AnswerValidator:

    def __init__(self, validators: list[BaseValidator]):
        self.validators = validators

    def validate(
        self,
        clue: SolverClueInput,
        answer: SolverAnswer,
    ) -> bool:

        #TODO make errors useful
        error_count = 0

        for validator in self.validators:
            is_valid = validator.validate(clue, answer)

            if not is_valid:
                error_count += 1

        return error_count == 0