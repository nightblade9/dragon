from dragon.transpilation.commands.add.add_indentation_curly_braces_command import AddIndentationCurlyBracesCommand
from dragon.transpilation.commands.add.add_package_statement_command import AddPackageStatementCommand
from dragon.transpilation.commands.substitute.transpile_class_declaration_command import TranspileClassDeclarationCommand
from dragon.transpilation.commands.substitute.transpile_function_declarations_command import TranspileFunctionDeclarationCommand
from dragon.transpilation.commands.substitute.transpile_import_statement_command import TranspileImportStatementCommand

"""
The main class that handles converting code from Python to Haxe.
It works on a file-by-file basis.
"""
class FileTransformer:

    def __init__(self, filename):
        self._filename = filename

    """
    Tranforms Python code to Haxe code.
    Returns the generated Haxe code.
    """
    def transform(self):
        with open(self._filename, "rt") as file:
            python_code = file.read()

        # TODO: super constructor calls (__init__ => new, super calls)
        pipeline_steps = [AddPackageStatementCommand(self._filename), TranspileImportStatementCommand(),
            TranspileClassDeclarationCommand(), AddIndentationCurlyBracesCommand(), TranspileFunctionDeclarationCommand()]

        code = python_code

        for step in pipeline_steps:
            code = step.execute(code)
        
        # TODO: simple token substitution, like elif => else if

        return code

