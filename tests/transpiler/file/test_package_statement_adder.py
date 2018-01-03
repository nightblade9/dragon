import distutils.dir_util
import os
import unittest
from dragon.transpiler.file.package_statement_adder import PackageStatementAdder

class TestPackageStatementAdder(unittest.TestCase):
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

    def test_add_package_statement_adds_empty_pacakge_for_root_file(self):
        file_path = "zomg_root_file.py"
        p = PackageStatementAdder()

        haxe_code = p.add_package_statement(file_path, TestPackageStatementAdder._MAIN_HX_PYTHON)
        self.assertIn("package;", haxe_code)

    def test_add_package_statement_adds_single_package_statement_for_one_subdirectory_file(self):
        p = PackageStatementAdder()

        haxe_code = p.add_package_statement(os.path.join("states", "main.py"), TestPackageStatementAdder._MAIN_HX_PYTHON)
        self.assertIn("package states;", haxe_code)

    def test_add_package_statement_adds_dot_delimited_pacakge_for_deep_file(self):
        p = PackageStatementAdder()
        haxe_code = p.add_package_statement(os.path.join("deengames", "owlicious", "core", "main.py"), TestPackageStatementAdder._MAIN_HX_PYTHON)

        self.assertIn("package deengames.owlicious.core", haxe_code)
        self.assertNotIn("package deengames.owlicious.core.element", haxe_code)
