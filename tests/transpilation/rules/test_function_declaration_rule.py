from dragon.transpilation.rules.substitute.function_declaration_rule import FunctionDeclarationRule
from dragon.transpilation.rules import line_substitution_rule
from helpers import test_data
import unittest

class TestFunctionDeclarationRule(unittest.TestCase):
    def test_execute_transforms_defs_into_functions_and_removes_self(self):
        rule = FunctionDeclarationRule()
        code = line_substitution_rule.apply(rule, test_data.MAIN_HX_PYTHON)
        self.assertIn("function __init__()", code) # def => function
        self.assertNotIn("function __init__(self)", code) # init(self) => init()
        self.assertNotIn("def __init__", code)