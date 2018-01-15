from dragon.transpiler.lark.lark_transpiler import LarkTranspiler
import os

class PythonToHaxeTranspiler:

    def __init__(self, source_path, files):
        self._source_path = source_path
        self._files = files

    def transpile(self):
        transpiler = LarkTranspiler()
        for filename in self._files:
            code = transpiler.transpile(filename)
            print("f={} s={}".format(filename, self._source_path))
            code = _add_package_statement(self._source_path, filename, code)
            self._convert_and_print(code, filename)              

    def _convert_and_print(self, code, filename):
        filename = filename.replace('.py', '.hx')
        with open(filename, 'wt') as f:
            f.write(code)

def _add_package_statement(source_root, path_and_filename, code, path_separator=os.path.sep):
    # eg. source_root = template\source, filename = template\source\main.py
    # Resulting package should be empty string. Subtract the two strings.
    filename = path_and_filename[0:path_and_filename.rindex(path_separator)]
    filename = filename.replace(source_root, "")
    # Sometimes the first character is a path separator that we don't want
    filename = filename[1:] if len(filename) and filename[0] == path_separator else filename
    package = filename.replace(path_separator, ".")
    code = "package {};\n{}".format(package, "\n".join(code))
    return code