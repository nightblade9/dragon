import distutils.dir_util
import os
import unittest
from dragon.transpiler.file.import_statement_transpiler import ImportStatementTranspiler

class TestImportStatementTranspiler(unittest.TestCase):
    MAIN_HX_PYTHON = """
from flixel.flx_game import FlxGame
from openfl.display.sprite import Sprite

class Main(Sprite):
    def __init__(self):
        super(Main, self).__init__()
        add_child(FlxGame(0, 0, PlayState))
"""

    def test_transpile_converts_import_statements(self):        
        t = ImportStatementTranspiler()
        haxe_code = t.transpile(TestImportStatementTranspiler.MAIN_HX_PYTHON)
        self.assertIn("import flixel.FlxGame;", haxe_code)
        self.assertIn("import openfl.display.Sprite;", haxe_code)