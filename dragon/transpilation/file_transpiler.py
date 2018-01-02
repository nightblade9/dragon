import re

class FileTranspiler:

    _PACKAGE_REGEX = "^package.*;"
    
    def __init__(self, haxe_code):
        self._haxe_code = haxe_code

    def transpile(self):
        output = self._haxe_code
        output = self._remove_packages(output)
        return output

    def _remove_packages(self, haxe_code):
        to_return = re.sub(FileTranspiler._PACKAGE_REGEX, "", haxe_code)
        return to_return        