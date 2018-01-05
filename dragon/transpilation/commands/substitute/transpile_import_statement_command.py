import re

class TranspileImportStatementCommand:
    # We only support newstyle "from x import y". Applied line by line.
    # The second grouping [a-zA-Z_] removes the final redundancy from the import
    # eg. "from openfl.display.sprite import Sprite" ignores ".sprite"
    _IMPORT_SEARCH_REGEX = r"^from ([a-zA-Z\._]+)\.[a-zA-Z_]+ import ([a-zA-Z_]+)"
    _IMPORT_REPLACEMENT_REGEX = r"import \1.\2;"

    """
    Converts imports of the form "from a.b.c import C" to "import a.b.C"
    """
    def execute(self, code):
        code = self._transform_imports(code)
        return code
    
    def _transform_imports(self, code):
        code_lines = code.splitlines()
        output = ""

        for line in code_lines:
            line = re.sub(TranspileImportStatementCommand._IMPORT_SEARCH_REGEX, TranspileImportStatementCommand._IMPORT_REPLACEMENT_REGEX, line)
            output = "{}\n{}".format(output, line)
        return output
