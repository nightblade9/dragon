from dragon.transpilation.rules.line_substitution_rule import LineSubstitutionRule

"""
Converts imports of the form "from a.b.c import C" to "import a.b.C"
"""
class ImportStatementRule(LineSubstitutionRule):
    # We only support newstyle "from x import y". Applied line by line.
    # The second grouping [a-zA-Z_] removes the final redundancy from the import
    # eg. "from openfl.display.sprite import Sprite" ignores ".sprite"
    _IMPORT_SEARCH_REGEX = r"^from ([a-zA-Z\._]+)\.[a-zA-Z_]+ import ([a-zA-Z_]+)"
    _IMPORT_REPLACEMENT_REGEX = r"import \1.\2;"

    def __init__(self):
        super(ImportStatementRule, self).__init__(
            ImportStatementRule._IMPORT_SEARCH_REGEX,
            ImportStatementRule._IMPORT_REPLACEMENT_REGEX)
