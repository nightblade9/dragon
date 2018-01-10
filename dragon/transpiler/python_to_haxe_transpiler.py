from dragon.transpiler.lark.lark_transpiler import LarkTranspiler

class PythonToHaxeTranspiler:

    def __init__(self, source_path, files):
        self._source_path = source_path
        self._files = files

    def transpile(self):
        transpiler = LarkTranspiler(self._source_path, self._files)
        transpiler.transpile()
