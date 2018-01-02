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

    def test_transpile_removes_package_statements(self):
        t = FileTranspiler(TestFileTranspiler.MAIN_HX)
        python_code = t.transpile()
        self.assertIsNone(re.search(FileTranspiler._PACKAGE_REGEX, python_code))

    def test_transpile_transforms_imports_into_python_style(self):
        t = FileTranspiler(TestFileTranspiler.MAIN_HX)
        python_code = t.transpile()

        haxe_imports = re.search(FileTranspiler._IMPORT_REGEX, python_code)
        self.assertIsNone(haxe_imports)

    ### End series ###