import distutils.dir_util
from helpers import test_data
import os
import unittest
from dragon.transpilation.commands.add_package_statement_command import AddPackageStatementCommand

class TestAddPackageStatementCommand(unittest.TestCase):
    ###
    # A series of "integration tests" that transpile the pythonified 
    # HaxeFlixel template (as of 4.3.0)
    ###

    def test_execute_adds_empty_pacakge_for_root_file(self):
        file_path = "zomg_root_file.py"
        p = AddPackageStatementCommand(file_path)

        haxe_code = p.execute(test_data.MAIN_HX_PYTHON)
        self.assertIn("package;", haxe_code)

    def test_execute_adds_single_package_statement_for_one_subdirectory_file(self):
        p = AddPackageStatementCommand(os.path.join("states", "main.py"))

        haxe_code = p.execute(test_data.MAIN_HX_PYTHON)
        self.assertIn("package states;", haxe_code)

    def test_execute_adds_dot_delimited_pacakge_for_deep_file(self):
        p = AddPackageStatementCommand(os.path.join("deengames", "owlicious", "core", "main.py"))
        haxe_code = p.execute(test_data.MAIN_HX_PYTHON)

        self.assertIn("package deengames.owlicious.core", haxe_code)
        self.assertNotIn("package deengames.owlicious.core.element", haxe_code)
