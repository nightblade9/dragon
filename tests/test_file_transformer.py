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
        t = FileTransformer(TestFileTransformer._MAIN_FILE_PATH)
        haxe_code = t.transform()
        print(haxe_code)
        # TODO: add qualitative tests