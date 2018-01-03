from dragon.transpiler.file.import_statement_transpiler import ImportStatementTranspiler
import os
import re

class FileTranspiler:

    ### TODO: split each operation into a separate class

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

        code = python_code
        code = self._add_package_statement(code)
        code = ImportStatementTranspiler().transpile(code)
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
