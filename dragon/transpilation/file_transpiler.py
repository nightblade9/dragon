import os
import re

class FileTranspiler:

    # We only support newstyle "from x import y". Applied line by line.
    # The second grouping [a-zA-Z_] removes the final redundancy from the import
    # eg. "from openfl.display.sprite import Sprite" ignores "sprite"
    _IMPORT_REGEX = r"^from ([a-zA-Z\._]+)\.[a-zA-Z_]+ import ([a-zA-Z_]+)"
    
    def __init__(self, filename):
        self._filename = filename

    def transpile(self):
        with open(self._filename, "rt") as file:
            python_code = file.read()

        # NB: the first transpile operation causes the rest of regex matches to fail
        # Probably something to do with newlines
        code = python_code
        code = self._add_package_statement(code)
        code = self._transform_imports(code)
        return code

    def _add_package_statement(self, code):
        path_only = os.path.split(self._filename)[0]
        packages = path_only.split(os.path.sep)
        package_statement = "package"

        if len(packages) and packages != [""]:
            package_statement = "package {}".format(".".join(packages))

        package_statement = "{};".format(package_statement)
        code = "{}\n{}".format(package_statement, code)
        return code

    def _transform_imports(self, code):
        code_lines = code.splitlines()        
        output = ""

        for line in code_lines:
            line = re.sub(FileTranspiler._IMPORT_REGEX, "import \\1.\\2;", line)
            output = "{}\n{}".format(output, line)
        return output
