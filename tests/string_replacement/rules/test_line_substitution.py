from dragon.string_replacement.rules import line_substitution
from tests.helpers import test_data
import unittest

class TestLineSubstitution(unittest.TestCase):
    def test_function_declaration_rule_transforms_defs_into_functions_and_removes_self(self):
        code = line_substitution.apply_regex(line_substitution.FUNCTION_DECLARATION_RULE, test_data.MAIN_HX_PYTHON)
        self.assertIn("function __init__()", code) # def => function
        self.assertNotIn("function __init__(self)", code) # init(self) => init()
        self.assertNotIn("def __init__", code)

    def test_import_statement_rule_converts_import_statements(self):
        code = line_substitution.apply_regex(line_substitution.IMPORT_STATEMENT_RULE, test_data.MAIN_HX_PYTHON)
        self.assertIn("import flixel.FlxGame;", code)
        self.assertIn("import openfl.display.Sprite;", code)