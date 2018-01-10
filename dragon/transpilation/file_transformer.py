from dragon.transpilation.commands.add.add_indentation_curly_braces_command import AddIndentationCurlyBracesCommand
from dragon.transpilation.commands.add.add_package_statement_command import AddPackageStatementCommand
from dragon.transpilation.commands.remove.remove_blank_lines_command import RemoveBlankLinesCommand
from dragon.transpilation.commands.substitute.transpile_class_declaration_command import TranspileClassDeclarationCommand
from dragon.transpilation.rules import line_substitution

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
        code = RemoveBlankLinesCommand.execute(code)
        code = AddPackageStatementCommand(self._filename).execute(code)
        code = line_substitution.apply_regex(line_substitution.IMPORT_STATEMENT_RULE, code)
        code = TranspileClassDeclarationCommand.execute(code)
        code = AddIndentationCurlyBracesCommand().execute(code)
        code = line_substitution.apply_regex(line_substitution.FUNCTION_DECLARATION_RULE, code)

        # TODO: simple token substitution, like elif => else if

        return code

