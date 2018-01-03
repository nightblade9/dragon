import os
import re

class FileTranspiler:

    ### TODO: split each operation into a separate class

    # We only support newstyle "from x import y". Applied line by line.
    # The second grouping [a-zA-Z_] removes the final redundancy from the import
    # eg. "from openfl.display.sprite import Sprite" ignores ".sprite"
    _IMPORT_SEARCH_REGEX = r"^from ([a-zA-Z\._]+)\.[a-zA-Z_]+ import ([a-zA-Z_]+)"
    _IMPORT_REPLACEMENT_REGEX = r"import \1.\2;"

    _CLASS_SEARCH_REGEX = r"class ([a-zA-Z]+)(\([a-zA-Z]+\))?:"
    _CLASS_REPLACEMENT_REGEX = r""

    def __init__(self, filename):
        self._filename = filename

    """
    Transpiles Python code to Haxe code.
    Returns the generated Haxe code.
    """
    def transpile(self):
        with open(self._filename, "rt") as file:
            python_code = file.read()

        # NB: the first transpile operation causes the rest of regex matches to fail
        # Probably something to do with newlines
        code = python_code
        code = self._add_package_statement(code)
        code = self._transform_imports(code)
        code = self._transform_class_declaration(code)
        return code

    """
    Adds a "package a.b.c;" statement depending on the file path.
    """
    def _add_package_statement(self, code):
        path_only = os.path.split(self._filename)[0]
        packages = path_only.split(os.path.sep)
        package_statement = "package"

        if len(packages) and packages != [""]:
            package_statement = "package {}".format(".".join(packages))

        package_statement = "{};".format(package_statement)
        code = "{}\n{}".format(package_statement, code)
        return code

    """
    Converts imports of the form "from a.b.c import C" to "import a.b.C"
    """
    def _transform_imports(self, code):
        code_lines = code.splitlines()
        output = ""

        for line in code_lines:
            line = re.sub(FileTranspiler._IMPORT_SEARCH_REGEX, FileTranspiler._IMPORT_REPLACEMENT_REGEX, line)
            output = "{}\n{}".format(output, line)
        return output

    def _transform_class_declaration(self, code):
        # TODO: what if it's just a module, not a class?
        output = code
        match = re.search(FileTranspiler._CLASS_SEARCH_REGEX, output)

        if (match):
            class_name = match.group(1)
            base_class = match.group(2)
            if base_class:
                base_class = base_class.replace('(', "").replace(')', "")
        
            base_class_declaration = " extends {}".format(base_class) if base_class else ""
            class_declaration = "class {}{} {{".format(class_name, base_class_declaration)
            
            output = output.replace(match.group(0), class_declaration)
        return output
