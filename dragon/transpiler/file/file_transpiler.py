from dragon.transpiler.file.class_declaration_transpiler import ClassDeclarationTranspiler
from dragon.transpiler.file.import_statement_transpiler import ImportStatementTranspiler
from dragon.transpiler.file.package_statement_adder import PackageStatementAdder

class FileTranspiler:

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
        code = PackageStatementAdder().add_package_statement(self._filename, code)
        code = ImportStatementTranspiler().transpile(code)
        code = ClassDeclarationTranspiler().transpile(code)
        return code

