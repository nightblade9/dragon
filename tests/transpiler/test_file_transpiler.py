import re
import unittest
from dragon.transpilation.file_transpiler import FileTranspiler

class TestFileTranspiler(unittest.TestCase):
    ###
    # A series of "integration tests" that transpile the HaxeFlixel template (as of 4.3.0)
    ###

    MAIN_HX = """package;

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

    MAIN_HX_AS_PYTHON = """
from flixel.flx_game import FlxGame
from openfl.display.sprite import Sprite

class Main(Sprite):
    def __init__(self):
        super(Main, self).__init__()
        add_child(FlxGame(0, 0, PlayState))
"""

    def test_transpile_removes_package_statements(self):
        t = FileTranspiler()
        python_code = t.transpile(TestFileTranspiler.MAIN_HX)
        self.assertIsNone(re.search(FileTranspiler._PACKAGE_REGEX, python_code))

    def test_transpile_transforms_imports_into_python_style(self):
        t = FileTranspiler()
        python_code = t.transpile(TestFileTranspiler.MAIN_HX)

        haxe_imports = re.search(FileTranspiler._IMPORT_REGEX, python_code)
        self.assertIsNone(haxe_imports)

        # Why isn't this failing? We didn't remove anything yet.

    ### End series ###