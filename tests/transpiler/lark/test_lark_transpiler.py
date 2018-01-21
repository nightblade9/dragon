from dragon.transpiler.lark.lark_transpiler import LarkTranspiler
from dragon.transpiler import transpilation_operations
from nose_parameterized import parameterized
import os
import unittest

"""
Integration tests that read files and expect the output to parse.
"""
class TestLarkCompiler(unittest.TestCase):

    _TEST_DATA_PATH = os.path.join("tests", "test_data")
    _EXPECTED_DATA_PATH = "expected"
    _INPUT_DATA_PATH = "input"

    @parameterized.expand([
        ["print_and_math.py"] # No semicolons in output?!
    ])
    def test_files_compile_as_expected(self, input_file):
        expected_file = transpilation_operations.python_name_to_haxe_name(input_file).replace(".py", ".hx")
        input_code = _read_contents(os.path.join(TestLarkCompiler._TEST_DATA_PATH, TestLarkCompiler._INPUT_DATA_PATH, input_file))
        expected_code = _read_contents(os.path.join(TestLarkCompiler._TEST_DATA_PATH, TestLarkCompiler._EXPECTED_DATA_PATH, expected_file))
        
        print(input_code)
        try:
            raw_code = LarkTranspiler().transpile(input_code)
            actual_code = "\n".join(raw_code)
        except:
            print("Failure parsing {}".format(input_file))
            raise

        self.assertEqual(expected_code, actual_code)

def _read_contents(fn, *args):
    kwargs = {'encoding': 'iso-8859-1'}
    with open(fn, *args, **kwargs) as f:
        return f.read()