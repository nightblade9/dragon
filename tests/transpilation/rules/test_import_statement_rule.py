from dragon.transpilation.rules.substitute.import_statement_rule import ImportStatementRule
from dragon.transpilation.rules import line_substitution_rule
import distutils.dir_util
from helpers import test_data
import os
import unittest

class TestImportStatementRule(unittest.TestCase):
    _MAIN_HX_PYTHON = """
from flixel.flx_game import FlxGame
from openfl.display.sprite import Sprite

class Main(Sprite):
    def __init__(self):
        super(Main, self).__init__()
        add_child(FlxGame(0, 0, PlayState))
"""

    def test_execute_converts_import_statements(self):
        rule = ImportStatementRule()
        code = line_substitution_rule.apply(rule, test_data.MAIN_HX_PYTHON)
        self.assertIn("import flixel.FlxGame;", code)
        self.assertIn("import openfl.display.Sprite;", code)