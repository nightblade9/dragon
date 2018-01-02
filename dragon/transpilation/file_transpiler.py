import re

class FileTranspiler:

    # Line-level regular expressions!
    _PACKAGE_REGEX = "^package.*;"
    _IMPORT_REGEX = "^import ([a-zA-Z]+)\.([a-zA-Z\.]);"
    
    def transpile(self, haxe_code):
        # NB: the first transpile operation causes the rest of regex matches to fail
        # Probably something to do with newlines
        python_code = haxe_code
        python_code = self._remove_packages(python_code)
        python_code = self._transform_imports(python_code)
        return python_code

    def _remove_packages(self, haxe_code):
        code_lines = haxe_code.splitlines()
        output = ""
        for line in code_lines:
            output = "{}\n{}".format(output, re.sub(FileTranspiler._PACKAGE_REGEX, "", line))
        return output

    def _transform_imports(self, haxe_code):
        code_lines = haxe_code.splitlines()
        output = ""
        for line in code_lines:
            match = re.search(FileTranspiler._IMPORT_REGEX, line)
            print("{} => {}".format(line, match))
            if match:
                print(match)
                pass
            output = "{}\n{}".format(output, line)
        return output