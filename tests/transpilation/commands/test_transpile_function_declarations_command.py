from dragon.transpilation.commands.transpile_function_declarations_command import TranspileFunctionDeclarationCommand
from helpers import test_data
import unittest

class TestTranspileFunctionDeclarationsCommand(unittest.TestCase):
    def test_execute_transforms_defs_into_functions_and_removes_self(self):
        command = TranspileFunctionDeclarationCommand()
        code = command.execute(test_data.MAIN_HX_PYTHON)
        self.assertIn("function __init__()", code) # def => function
        self.assertNotIn("function __init__(self)", code) # init(self) => init()
        self.assertNotIn("def __init__", code)