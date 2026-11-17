import unittest

from llm_cw.domain.validator import _validate_positional_constraints

class TestValidatePositionalConstraints(unittest.TestCase):
    def test_valid_constraints(self):
        """CAT is valid when first letter must be C"""
        answer_text = 'CAT'
        positional_constraints = {0:'C'}

        result = _validate_positional_constraints(answer_text,
                                                  positional_constraints)

        self.assertTrue(result)

    def test_invalid_constraints(self):
        """PAT is invalid when 1st letter must be C"""
        answer_text = 'PAT'
        positional_constraints = {0:'C'}

        result = _validate_positional_constraints(answer_text,
                                                    positional_constraints)

        self.assertFalse(result)

    def test_empty_constraints(self):
        """Any answer should be valid if there are no positional constraints"""
        answer_text = 'PAT'
        positional_constraints = {}

        result = _validate_positional_constraints(answer_text,
                                                    positional_constraints)

        self.assertTrue(result)

    def test_length_agnostic(self):
        """this validator should only be checking constraints, not length"""
        answer_text = 'PAT' # answer only 3 letters
        positional_constraints = {5:'X'} # 6th letter is X

        result = _validate_positional_constraints(answer_text,
                                                    positional_constraints)
        self.assertFalse(result)

    def test_empty_answer_non_empty_constraint(self):
        """empty answer should return False"""
        answer_text = ''
        positional_constraints = {0:"C"}
        result = _validate_positional_constraints(answer_text,
                                                  positional_constraints)
        self.assertFalse(result)

    def test_empty_answer_empty_constraint(self):
            """empty answer should return False"""
            answer_text = ''
            positional_constraints = {}
            result = _validate_positional_constraints(answer_text,
                                                      positional_constraints)
            self.assertTrue(result)
    