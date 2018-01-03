import distutils.dir_util
import os
import unittest
from dragon.transpiler.file.file_transpiler import FileTranspiler

class TestFileTranspiler(unittest.TestCase):
    ###
    # A series of "integration tests" that transpile the pythonified 
    # HaxeFlixel template (as of 4.3.0)
    ###

    _TEST_FILE_DIR = "temp"
    _MAIN_FILE_PATH = os.path.join(_TEST_FILE_DIR, "main.py")

    MAIN_HX_PYTHON = """
from flixel.flx_game import FlxGame
from openfl.display.sprite import Sprite

class Main(Sprite):
    def __init__(self):
        super(Main, self).__init__()
        add_child(FlxGame(0, 0, PlayState))
"""

    def setUp(self):
        os.makedirs(TestFileTranspiler._TEST_FILE_DIR)        

    def tearDown(self):
        os.remove(TestFileTranspiler._MAIN_FILE_PATH)
        os.removedirs(TestFileTranspiler._TEST_FILE_DIR)

    def test_transpile_converts_classes_and_base_class(self):
        with open(TestFileTranspiler._MAIN_FILE_PATH, "wt") as file:
            file.write(TestFileTranspiler.MAIN_HX_PYTHON)

        t = FileTranspiler(TestFileTranspiler._MAIN_FILE_PATH)
        haxe_code = t.transpile()
        self.assertIn("class Main extends Sprite {", haxe_code)

    def test_transpile_exlcudes_base_class_for_non_derived_classes(self):
        # Replace main.py with a non-derived class
        python_code = TestFileTranspiler.MAIN_HX_PYTHON.replace("class Main(Sprite):", "class Awesome:")

        with open(TestFileTranspiler._MAIN_FILE_PATH, "wt") as file:
            file.write(python_code)

        t = FileTranspiler(TestFileTranspiler._MAIN_FILE_PATH)
        haxe_code = t.transpile()
        self.assertIn("class Awesome {", haxe_code)
      