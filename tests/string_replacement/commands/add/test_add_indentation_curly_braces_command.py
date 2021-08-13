from dragon.string_replacement.commands.add.add_indentation_curly_braces_command import AddIndentationCurlyBracesCommand
from dragon.string_replacement.commands.substitute.transpile_class_declaration_command import TranspileClassDeclarationCommand
from tests.helpers import test_data
import unittest

class TestAddIndentationCurlyBracesCommand(unittest.TestCase):
    def test_execute_adds_all_curly_braces_required(self):
        command = AddIndentationCurlyBracesCommand()
        # Not necessary but makes it easier to read the final code
        code = TranspileClassDeclarationCommand.execute(test_data.MAIN_HX_PYTHON)
        code = command.execute(code)

        self.assertEqual(code.count("{"), code.count("}")) # equal braces
        self.assertIn("class Main extends Sprite {", code) # class declaration has a brace
        self.assertIn("def __init__(self): {", code) # method has an opening brace
        self.assertEqual(code[-1], "}") # class has a closing brace

    def test_execute_adds_multiple_close_braces_if_multiple_levels_drop(self):
        # code jumps from inside-def to empty-line, that's two levels.
        # The last two lines should progressively close braces.
        code = AddIndentationCurlyBracesCommand().execute(test_data.MAIN_HX_PYTHON)
        lines = code.splitlines()
        self.assertIn("    }", lines[-2])
        self.assertIn("}", lines[-1])