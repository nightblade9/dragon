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

    MAIN_HX_EXPECTED = """package;

import flixel.FlxGame;
import openfl.display.Sprite;

class Main extends Sprite {
	public function new() {
		super();
		addChild(new FlxGame(0, 0, PlayState));
	}
}
"""

    def setUp(self):
        os.makedirs(TestFileTranspiler._TEST_FILE_DIR)
        with open(TestFileTranspiler._MAIN_FILE_PATH, "wt") as file:
            file.write(TestFileTranspiler.MAIN_HX_PYTHON)

    def tearDown(self):
        os.remove(TestFileTranspiler._MAIN_FILE_PATH)
        os.removedirs(TestFileTranspiler._TEST_FILE_DIR)

    def test_transpile_adds_empty_pacakge_for_root_file(self):
        file_path = "zomg_root_file.py"
        with open(file_path, "wt") as file:
            file.write(TestFileTranspiler.MAIN_HX_PYTHON)
        try:
            t = FileTranspiler(file_path)
            haxe_code = t.transpile()
            self.assertIn("package;", haxe_code)
        finally:
            os.remove(file_path)

    def test_transpile_adds_single_package_statement_for_one_subdirectory_file(self):
        t = FileTranspiler(TestFileTranspiler._MAIN_FILE_PATH)
        haxe_code = t.transpile()
        self.assertIn("package temp;", haxe_code)

    def test_transpile_adds_dot_delimited_pacakge_for_deep_file(self):
        file_path = os.path.join("deengames", "owlicious", "core", "element.py")
        distutils.dir_util.create_tree(file_path[0:-1], file_path[-1])

        with open(file_path, "wt") as file:
            file.write(TestFileTranspiler.MAIN_HX_PYTHON)
        try:
            t = FileTranspiler(file_path)
            haxe_code = t.transpile()
            self.assertIn("package deengames.owlicious.core", haxe_code)
            self.assertNotIn("package deengames.owlicious.core.element", haxe_code)
        finally:
            path_only = os.path.split(file_path)[0]
            os.remove(file_path)

    def test_transpile_converts_import_statements(self):
        t = FileTranspiler(TestFileTranspiler._MAIN_FILE_PATH)
        haxe_code = t.transpile()
        self.assertIn("import flixel.FlxGame;", haxe_code)
        self.assertIn("import openfl.display.Sprite;", haxe_code)

    def test_transpile_converts_classes_and_base_class(self):
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

    ### End series ###
