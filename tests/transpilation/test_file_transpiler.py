import os
import unittest
from dragon.transpilation.file_transpiler import FileTranspiler

class TestFileTranspiler(unittest.TestCase):

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
        os.makedirs(TestFileTranspiler._TEST_FILE_DIR)
        with open(TestFileTranspiler._MAIN_FILE_PATH, "wt") as file:
            file.write(TestFileTranspiler._MAIN_HX_PYTHON)

    def tearDown(self):
        os.remove(TestFileTranspiler._MAIN_FILE_PATH)
        os.removedirs(TestFileTranspiler._TEST_FILE_DIR)

    def test_transpile_transpiles_main_py_to_haxe(self):
        t = FileTranspiler(TestFileTranspiler._MAIN_FILE_PATH)
        haxe_code = t.transpile()
        print(haxe_code)
        # TODO: add qualitative tests