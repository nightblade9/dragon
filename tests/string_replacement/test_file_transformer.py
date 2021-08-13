from dragon.string_replacement.file_transformer import FileTransformer
from tests.helpers import test_data
import os
import unittest

class TestFileTransformer(unittest.TestCase):

    # Integration-test like test that expects a file, does some qualitative testing
    # For individual units (commands), see their respective command test-classes

    _TEST_FILE_DIR = "temp"
    _MAIN_FILE_PATH = os.path.join(_TEST_FILE_DIR, "main.py")

    def setUp(self):
        # Not Pythonic (EAFP) but fails often locally when you add print statements
        # This makes our test runs much more reliable.
        if not os.path.exists(TestFileTransformer._TEST_FILE_DIR):
            os.makedirs(TestFileTransformer._TEST_FILE_DIR)

        with open(TestFileTransformer._MAIN_FILE_PATH, "wt") as file:
            file.write(test_data.MAIN_HX_PYTHON)

    def tearDown(self):
        os.remove(TestFileTransformer._MAIN_FILE_PATH)
        os.removedirs(TestFileTransformer._TEST_FILE_DIR)

    def test_transpile_correctly_transpiles_multiple_functions(self):
        # Test a bug where the class generated a closing brace, although there
        # are more functions below it.
        with open(TestFileTransformer._MAIN_FILE_PATH, "at") as file:
            file.write("""


    def second_function(self):
        print("HI!")
""")

        t = FileTransformer(TestFileTransformer._MAIN_FILE_PATH)
        haxe_code = t.transform()
        code_lines = [line.rstrip() for line in haxe_code.splitlines() if len(line.strip()) > 0]
        
        first_closing_brace = _get_line_number(code_lines, "    }")
        next_line = code_lines[first_closing_brace + 1]
        self.assertIn("function", next_line)
        self.assertNotIn("}", next_line)

    def test_transpile_transpiles_main_py_to_haxe(self):
        # A series of tests for integration things, eg. class + brackets = "class X { ... }"
        t = FileTransformer(TestFileTransformer._MAIN_FILE_PATH)
        haxe_code = t.transform()

        # Remove empty lines and trailing spaces
        code_lines = [line.rstrip() for line in haxe_code.splitlines() if len(line.strip()) > 0]

        self.assertIn("package temp;", code_lines[0]) # package is first line
        self.assertIn("import flixel.FlxGame;", haxe_code) # import
        self.assertIn("class Main extends Sprite {", haxe_code) # class + brace
        #self.assertIn("function new() {", haxe_code) # initializer => constructor
        #self.assertIn("super();", haxe_code) # Pythonic constructor format change
        #self.assertIn("add_child(new FlxGame(0, 0, PlayState));", haxe_code) # final semicolon, constructor calls
        self.assertIn("    }", code_lines[-2])
        self.assertEqual("}", code_lines[-1])

def _get_line_number(lines, search):
    for num, line in enumerate(lines):
        if line == search:
            return num

    raise LookupError("Can't find {} in {}".format(search, lines))