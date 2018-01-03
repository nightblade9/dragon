import distutils.dir_util
import os
import unittest
from dragon.transpilation.commands.transpile_import_statement_command import TranspileImportStatementCommand

class TestTranspileImportStatementCommand(unittest.TestCase):
    MAIN_HX_PYTHON = """
from flixel.flx_game import FlxGame
from openfl.display.sprite import Sprite

class Main(Sprite):
    def __init__(self):
        super(Main, self).__init__()
        add_child(FlxGame(0, 0, PlayState))
"""

    def test_execute_converts_import_statements(self):        
        t = TranspileImportStatementCommand()
        haxe_code = t.execute(TestTranspileImportStatementCommand.MAIN_HX_PYTHON)
        self.assertIn("import flixel.FlxGame;", haxe_code)
        self.assertIn("import openfl.display.Sprite;", haxe_code)