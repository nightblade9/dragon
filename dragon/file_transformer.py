from dragon.transpilation.commands.add.add_indentation_curly_braces_command import AddIndentationCurlyBracesCommand
from dragon.transpilation.commands.add.add_package_statement_command import AddPackageStatementCommand
from dragon.transpilation.commands.substitute.transpile_class_declaration_command import TranspileClassDeclarationCommand
from dragon.transpilation.rules import line_substitution_rule
from dragon.transpilation.rules.substitute.function_declaration_rule import FunctionDeclarationRule
from dragon.transpilation.rules.substitute.import_statement_rule import ImportStatementRule

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

        code = python_code
        code = AddPackageStatementCommand(self._filename).execute(code)
        code = line_substitution_rule.apply(ImportStatementRule(), code)
        code = TranspileClassDeclarationCommand().execute(code)
        code = AddIndentationCurlyBracesCommand().execute(code)
        code = line_substitution_rule.apply(FunctionDeclarationRule(), code)

        # TODO: simple token substitution, like elif => else if

        return code

