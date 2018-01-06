import distutils.dir_util
from dragon.transpilation.commands.substitute.transpile_class_declaration_command import TranspileClassDeclarationCommand
from helpers import test_data

import os
import unittest

class TestTranspileClassDeclarationCommand(unittest.TestCase):
    ###
    # A series of "integration tests" that transpile the pythonified 
    # HaxeFlixel template (as of 4.3.0)
    ###

    _MAIN_HX_PYTHON = """
from flixel.flx_game import FlxGame
from openfl.display.sprite import Sprite

class Main(Sprite):
    def __init__(self):
        super(Main, self).__init__()
        add_child(FlxGame(0, 0, PlayState))
"""

    def test_transpile_converts_classes_and_base_class(self):
        haxe_code = TranspileClassDeclarationCommand.execute(test_data.MAIN_HX_PYTHON)
        self.assertIn("class Main extends Sprite", haxe_code)

    def test_transpile_exlcudes_base_class_for_non_derived_classes(self):
        # Replace main.py with a non-derived class
        python_code = test_data.MAIN_HX_PYTHON.replace("class Main(Sprite):", "class Awesome:")
        haxe_code = TranspileClassDeclarationCommand.execute(python_code)
        self.assertIn("class Awesome", haxe_code)
        self.assertNotIn("class Awesome extends", haxe_code)
      