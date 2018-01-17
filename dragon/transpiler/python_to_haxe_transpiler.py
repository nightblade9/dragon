from dragon.transpiler.lark.lark_transpiler import LarkTranspiler
from dragon.transpiler import transpilation_operations

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

    def _convert_and_print(self, code, filename):
        filename = filename.replace('.py', '.hx')
        filename = transpilation_operations.camel_case_to_pep8_method_name(filename)
        print("Writing {}".format(filename))
        with open(filename, 'wt') as f:
            f.write(code)

