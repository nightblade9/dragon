from dragon.transpilation.commands.add_indentation_curly_braces_command import AddIndentationCurlyBracesCommand
from dragon.transpilation.commands.add_package_statement_command import AddPackageStatementCommand
from dragon.transpilation.commands.transpile_class_declaration_command import TranspileClassDeclarationCommand
from dragon.transpilation.commands.transpile_function_declarations_command import TranspileFunctionDeclarationCommand
from dragon.transpilation.commands.transpile_import_statement_command import TranspileImportStatementCommand

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
        code = AddPackageStatementCommand().execute(self._filename, code)
        code = TranspileImportStatementCommand().execute(code)
        code = TranspileClassDeclarationCommand().execute(code)
        code = AddIndentationCurlyBracesCommand().execute(code)
        code = TranspileFunctionDeclarationCommand().execute(code)
        # super constructor calls (__init__ => new, super calls)
        return code

