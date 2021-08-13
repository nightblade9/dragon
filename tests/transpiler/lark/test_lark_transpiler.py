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
    # Premature optimiziation is the root of much evil. In this case, when
    # transpiling a bunch of files, each file takes ~1s. It turns out that
    # invoking this constructor (which parses the Python 3 grammar) takes
    # pretty much 95-99% of that 1s. So keeping an instance here greatly
    # speeds up transpilation of files for multiple test-cases.
    _TRANSPILER = LarkTranspiler()

    @parameterized.expand([
        ["print_and_math.py"], # Basic print statements and math. No semicolons in output?!
        # Generators and generator comprehensions are really complicated to implement.
        # For now, skip this file.
        # ["generators_and_comprehensions.py"], 
        # Boilerplate files that are the same in all HaxeFlixel templates
        ["haxeflixel_template_main.py"],
        ["haxeflixel_template_asset_paths.py"], # No semicolons in output?!
        # HaxeFlixel templates (usually a single PlayState.hx file)
        ["haxeflixel_template_default_playstate.py"] # Default
    ])
    def test_files_compile_as_expected(self, input_file):
        expected_file = transpilation_operations.python_name_to_haxe_name(input_file).replace(".py", ".hx")
        input_code = _read_contents(os.path.join(TestLarkCompiler._TEST_DATA_PATH, TestLarkCompiler._INPUT_DATA_PATH, input_file))
        expected_code = _read_contents(os.path.join(TestLarkCompiler._TEST_DATA_PATH, TestLarkCompiler._EXPECTED_DATA_PATH, expected_file))

        try:
            raw_code = TestLarkCompiler._TRANSPILER.transpile(input_code)
            actual_code = "\n".join(raw_code)
        except:
            print("Failure parsing {}".format(input_file))
            raise

        self.assertEqual(expected_code, actual_code)


def _read_contents(fn, *args):
    kwargs = {'encoding': 'iso-8859-1'}
    with open(fn, *args, **kwargs) as f:
        return f.read()