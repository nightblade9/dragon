import distutils.dir_util
import os
import unittest
from dragon.transpilation.file_transpiler import FileTranspiler

class TestFileTranspiler(unittest.TestCase):
    ###
    # A series of "integration tests" that transpile the pythonified 
    # HaxeFlixel template (as of 4.3.0)
    ###

    MAIN_HX_EXPECTED = """package;

import flixel.FlxGame;
import openfl.display.Sprite;

class Main extends Sprite
{
	public function new()
	{
		super();
		addChild(new FlxGame(0, 0, PlayState));
	}
}
"""

    MAIN_HX_PYTHON = """
from flixel.flx_game import FlxGame
from openfl.display.sprite import Sprite

class Main(Sprite):
    def __init__(self):
        super(Main, self).__init__()
        add_child(FlxGame(0, 0, PlayState))
"""

    def test_transpile_adds_empty_package_statement_for_root_file(self):
        with open("main.py", "wt") as file:
            file.write(TestFileTranspiler.MAIN_HX_PYTHON)
        try:
            t = FileTranspiler("main.py")
            haxe_code = t.transpile()
            self.assertTrue("package;" in haxe_code)
        except:
            os.remove("main.py")
            raise

    def test_transpile_adds_dot_delimited_pacakge_for_deep_file(self):
        file_path = os.path.join("deengames", "owlicious", "core", "element.py")
        distutils.dir_util.create_tree(file_path[0:-1], file_path[-1])

        with open(file_path, "wt") as file:
            file.write(TestFileTranspiler.MAIN_HX_PYTHON)
        try:
            t = FileTranspiler(file_path)
            haxe_code = t.transpile()
            self.assertTrue("package deengames.owlicious.core" in haxe_code)
            self.assertTrue("package deengames.owlicious.core.element" not in haxe_code)
        except:
            path_only = os.path.split(file_path)[0]
            os.remove(file_path)
            distutils.dir_util.remove_tree(path_only)            
            raise

    ### End series ###