from lark import Lark
import os
from .python_indenter import PythonIndenter
import sys
from .transformers.haxe_transformer import HaxeTransformer

class LarkTranspiler:
    
    _PYTHON_3_GRAMMAR_FILENAME = 'python3.g'
    # TODO: try PyPy, etc. once you get a large enough code-base to test against
    _PARSER = "lalr"
    _PARSER_START = 'file_input'

    def __init__(self, source_path, files):
        self._source_path = source_path
        self._files = files
        
        grammar_path = sys.modules[__name__].__file__
        grammar_path = grammar_path[:grammar_path.rindex(os.path.sep)]
        grammar_filename = os.path.join(grammar_path, LarkTranspiler._PYTHON_3_GRAMMAR_FILENAME)

        with open(grammar_filename) as f:
            self._python_parser = Lark(f, parser=LarkTranspiler._PARSER, postlex=PythonIndenter(), start=LarkTranspiler._PARSER_START)

    def transpile(self):
        for filename in self._files:
            try:
                tree = self._python_parser.parse(_read_contents(filename) + '\n')
                tree = HaxeTransformer().transform(tree)
                _convert_and_print(tree, filename)              
            except:
                print ('Failure parsing %s' % filename)
                raise

def _convert_and_print(tree, filename):
    filename = filename.replace('.py', '.hx')
    with open(filename, 'wt') as f:
        f.write(tree.pretty())

def _read_contents(fn, *args):
    kwargs = {'encoding': 'iso-8859-1'}
    with open(fn, *args, **kwargs) as f:
        return f.read()
