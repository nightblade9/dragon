from dragon.transpiler.python_to_haxe_transpiler import PythonToHaxeTranspiler
from dragon.transpiler import transpilation_operations
from nose_parameterized import parameterized
import os
import unittest

class TestTranspilationOperations(unittest.TestCase):
    def test_add_package_statement_adds_empty_statement_for_root_file(self):
        # Linux style path
        code = transpilation_operations.add_package_statement("/tmp", "/tmp/main.hx", "", "/")
        self.assertIn("package ;", code)

    def test_add_package_statement_adds_single_package(self):
        # Windows style path
        code = transpilation_operations.add_package_statement("C:\\project",
            "C:\\project\\models\\player.py", "", "\\")
        self.assertIn("package models;", code)

    def test_add_package_statement_adds_multiple_nested_packages(self):
        root = os.path.join("projects", "haxe", "samurai", "code")
        filename = os.path.join(root, "common", "models", "entities", "player.py")
        code = transpilation_operations.add_package_statement(root, filename, "")
        self.assertIn("package common.models.entities", code)
    
    @parameterized.expand([
        ["lower", "lower"],
        ["addChild", "add_child"],
        ["ALL_UPPER", "all_upper"],
        ["partial_UPPER", "partial_upper"],
        ["one_TWO3_four", "one_two3_four"]
    ])
    def test_camel_case_to_pep8_method_name_works_as_expected(self, input_string, expected):
        output = transpilation_operations.camel_case_to_pep8_method_name(input_string)
        self.assertEqual(expected, output)
