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

        # TODO: super constructor calls (__init__ => new, super calls)
        pipeline_steps = [AddPackageStatementCommand(self._filename), TranspileImportStatementCommand(),
            TranspileClassDeclarationCommand(), AddIndentationCurlyBracesCommand(), TranspileFunctionDeclarationCommand()]

        code = python_code

        for step in pipeline_steps:
            code = step.execute(code)
        
        return code

