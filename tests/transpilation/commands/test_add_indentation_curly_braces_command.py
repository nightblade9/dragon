from dragon.transpilation.commands.add_indentation_curly_braces_command import AddIndentationCurlyBracesCommand
from dragon.transpilation.commands.transpile_class_declaration_command import TranspileClassDeclarationCommand
from helpers import test_data
import unittest

class TestAddIndentationCurlyBracesCommand(unittest.TestCase):
    def test_execute_adds_all_curly_braces_required(self):
        command = AddIndentationCurlyBracesCommand()
        # Not necessary but makes it easier to read the final code
        code = TranspileClassDeclarationCommand().execute(test_data.MAIN_HX_PYTHON)
        code = command.execute(code)

        self.assertEqual(code.count("{"), code.count("}")) # equal braces
        self.assertIn("class Main extends Sprite {", code) # class declaration has a brace
        self.assertIn("def __init__(self): {", code) # method has an opening brace
        self.assertEqual(code[-1], "}") # class has a closing brace