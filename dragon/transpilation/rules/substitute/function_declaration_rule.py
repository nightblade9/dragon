from dragon.transpilation.rules.line_substitution_rule import LineSubstitutionRule

# Transpiles def(self, ...) => function(...) or def(...) => function(...)
class FunctionDeclarationRule(LineSubstitutionRule):

    # Not just the "def", but also removes arguments ... including "self"
    _FUNCTION_DECLARATION_SEARCH_REGEX = r"def ([a-zA-Z0-9_]+)(\([a-zA-Z0-9_, ]+\))?:"
    _FUNCTION_DECLARATION_REPLACEMENT_REGEX = r"function \1()"

    # TODO: remove "self" from argument if present
    # TODO: Put that into a second rule?
    def __init__(self):
        super(FunctionDeclarationRule, self).__init__(
            FunctionDeclarationRule._FUNCTION_DECLARATION_SEARCH_REGEX,
            FunctionDeclarationRule._FUNCTION_DECLARATION_REPLACEMENT_REGEX)
