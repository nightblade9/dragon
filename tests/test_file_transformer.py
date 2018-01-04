import os
import unittest
from dragon.file_transformer import FileTransformer

class TestFileTransformer(unittest.TestCase):

    # Integration-test like test that expects a file, does some qualitative testing
    # For individual units (commands), see their respective command test-classes

    _TEST_FILE_DIR = "temp"
    _MAIN_FILE_PATH = os.path.join(_TEST_FILE_DIR, "main.py")

    _MAIN_HX_PYTHON = """
from flixel.flx_game import FlxGame
from openfl.display.sprite import Sprite

class Main(Sprite):
    def __init__(self):
        super(Main, self).__init__()
        add_child(FlxGame(0, 0, PlayState))
"""

    def setUp(self):
        os.makedirs(TestFileTransformer._TEST_FILE_DIR)
        with open(TestFileTransformer._MAIN_FILE_PATH, "wt") as file:
            file.write(TestFileTransformer._MAIN_HX_PYTHON)

    def tearDown(self):
        os.remove(TestFileTransformer._MAIN_FILE_PATH)
        os.removedirs(TestFileTransformer._TEST_FILE_DIR)

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