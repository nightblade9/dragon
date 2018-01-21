from dragon.validators import lark_validator
from dragon.validators.lark_validator import LarkValidator
from lark.lexer import Token
from lark import Tree
import os
import unittest

class TestLarkValidator(unittest.TestCase):

    _GRAMMAR_LOCATION = os.path.join("dragon", "transpiler", "lark", "python3.g")

    def test_is_fully_parsed_returns_true_if_all_tokens_are_transformed(self):
        # Just a bunch of tokens, like "super", "update", "elapsed"
        tree = Tree("getattr", ['super', Token("NAME", 'update')]).pretty()
        validator = LarkValidator(TestLarkValidator._GRAMMAR_LOCATION)
        self.assertTrue(validator.is_fully_parsed(tree))
        
    def test_is_fully_parsed_returns_false_if_tree_in_code(self):
        # Just a bunch of tokens, like "super", "update", "elapsed"
        code = ["Regular code line", Tree("FAIL_NODE", "x"), "More regular code"]
        validator = LarkValidator(TestLarkValidator._GRAMMAR_LOCATION)
        self.assertFalse(validator.is_fully_parsed(code))

    def test_validate_class_definition_allows_empty_base_class(self):
        # Doesn't throw
        lark_validator.validate_class_definition("Entity", [])

    def test_validate_class_definition_allows_one_base_class(self):
        # Doesn't throw
        lark_validator.validate_class_definition("Player", ["Entity"])

    def test_validate_class_definition_throws_if_multiple_base_classes_are_specified(self):
        with self.assertRaises(ValueError) as ex:
            lark_validator.validate_class_definition("Player", ["Entity", "FlxSprite"])
