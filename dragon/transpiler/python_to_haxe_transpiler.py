from dragon.transpiler.lark.lark_transpiler import LarkTranspiler
from dragon.transpiler import transpilation_operations
import os

class PythonToHaxeTranspiler:

    def __init__(self, source_path, files):
        self._source_path = source_path
        self._files = files

    def transpile(self):
        transpiler = LarkTranspiler()
        for filename in self._files:
            code = transpiler.transpile(filename)
            code = transpilation_operations.add_package_statement(self._source_path, filename, code)
            self._convert_and_print(code, filename)              

    def _convert_and_print(self, code, path_and_filename):
        finalSeparator = path_and_filename.rindex(os.path.sep) + 1
        filename = path_and_filename[finalSeparator:]
        original_filename = path_and_filename
        filename = filename.replace('.py', '.hx')
        filename = transpilation_operations.python_name_to_haxe_name(filename)
        path_and_filename = "{}{}".format(path_and_filename[0:finalSeparator], filename)
        print("Converted {} => {}".format(original_filename, filename))
        with open(path_and_filename, 'wt') as f:
            f.write(code)

