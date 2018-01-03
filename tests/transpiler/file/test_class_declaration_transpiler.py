import distutils.dir_util
import os
import unittest
from dragon.transpiler.file.class_declaration_transpiler import ClassDeclarationTranspiler

class TestClassDeclarationTranspiler(unittest.TestCase):
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
        t = ClassDeclarationTranspiler()
        haxe_code = t.transpile(TestClassDeclarationTranspiler._MAIN_HX_PYTHON)
        self.assertIn("class Main extends Sprite {", haxe_code)

    def test_transpile_exlcudes_base_class_for_non_derived_classes(self):
        # Replace main.py with a non-derived class
        python_code = TestClassDeclarationTranspiler._MAIN_HX_PYTHON.replace("class Main(Sprite):", "class Awesome:")
        t = ClassDeclarationTranspiler()
        haxe_code = t.transpile(python_code)
        self.assertIn("class Awesome {", haxe_code)
      