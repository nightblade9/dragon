from dragon.transpiler.lark.lark_transpiler import LarkTranspiler

class PythonToHaxeTranspiler:

    def __init__(self, source_path, files):
        self._source_path = source_path
        self._files = files

    def transpile(self):
        transpiler = LarkTranspiler()
        for filename in self._files:
            code = transpiler.transpile(filename)
            self._convert_and_print(code, filename)              

    def _convert_and_print(self, code, filename):
        filename = filename.replace('.py', '.hx')
        with open(filename, 'wt') as f:
            f.write("\n".join(code))
