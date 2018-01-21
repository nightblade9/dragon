from lark import Lark
from dragon.transpiler.lark.python_indenter import PythonIndenter
from dragon.transpiler.lark.transformers.haxe_transformer import HaxeTransformer
import os
import sys

class LarkTranspiler:
    
    _PYTHON_3_GRAMMAR_FILENAME = 'python3.g'
    # TODO: try PyPy, etc. once you get a large enough code-base to test against
    _PARSER = "lalr"
    _PARSER_START = 'file_input'

    def __init__(self):
        grammar_path = sys.modules[__name__].__file__
        grammar_path = grammar_path[:grammar_path.rindex(os.path.sep)]
        self.grammar_filename = os.path.join(grammar_path, LarkTranspiler._PYTHON_3_GRAMMAR_FILENAME)

        with open(self.grammar_filename) as f:
            self._python_parser = Lark(f, parser=LarkTranspiler._PARSER, postlex=PythonIndenter(), start=LarkTranspiler._PARSER_START)

    def transpile(self, raw_file_text):
        tree = self._python_parser.parse(raw_file_text)
        code = HaxeTransformer().transform(tree)
        return code
