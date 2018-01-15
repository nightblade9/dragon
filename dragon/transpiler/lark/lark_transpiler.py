from lark import Lark
from .python_indenter import PythonIndenter
from .transformers.haxe_transformer import HaxeTransformer
from .validators.lark_validator import LarkValidator
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

    def transpile(self, filename):
        try:
            tree = self._python_parser.parse(_read_contents(filename) + '\n')
            code = HaxeTransformer().transform(tree)
        except:
            print ('Failure parsing %s' % filename)
            raise

        validator = LarkValidator(self.grammar_filename)
        if not validator.is_fully_parsed(code):
            raise NotImplementedError("{} is not fully parsable.".format(filename))

        return code

def _read_contents(fn, *args):
    kwargs = {'encoding': 'iso-8859-1'}
    with open(fn, *args, **kwargs) as f:
        return f.read()
