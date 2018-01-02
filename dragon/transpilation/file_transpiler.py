import re

class FileTranspiler:

    # Line-level regular expressions!
    _PACKAGE_REGEX = "^package.*;"
    _IMPORT_REGEX = "^import ([a-zA-Z]+)\.([a-zA-Z\.]);"
    
    def __init__(self, haxe_code):
        # Combine into lines; we operate line-by-line later.
        self._code_lines = haxe_code.splitlines()

    def transpile(self):
        self._remove_packages()
        self._transform_imports()
        return "".join(self._code_lines)

    def _remove_packages(self):        
        for index, line in enumerate(self._code_lines):
            self._code_lines[index] = re.sub(FileTranspiler._PACKAGE_REGEX, "", line)

    def _transform_imports(self):
        for index, line in enumerate(self._code_lines):
            self._code_lines[index] = re.sub(FileTranspiler._IMPORT_REGEX, "from \1 import \2", line)