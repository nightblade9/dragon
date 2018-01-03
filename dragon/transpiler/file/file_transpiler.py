from dragon.transpiler.file.import_statement_transpiler import ImportStatementTranspiler
from dragon.transpiler.file.class_declaration_transpiler import ClassDeclarationTranspiler
import os
import re

class FileTranspiler:

    ### TODO: split each operation into a separate class

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
        code = ClassDeclarationTranspiler().transpile(code)
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

