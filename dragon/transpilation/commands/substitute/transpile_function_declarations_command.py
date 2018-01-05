import re

class TranspileFunctionDeclarationCommand:

    _FUNCTION_DECLARATION_SEARCH_REGEX = r"def ([a-zA-Z0-9_]+)"
    _FUNCTION_DECLARATION_REPLACEMENT_REGEX = r"function \1"

    def execute(self, code):
        code_lines = code.splitlines()
        output = ""

        for line in code_lines:
            if re.search(TranspileFunctionDeclarationCommand._FUNCTION_DECLARATION_SEARCH_REGEX, line):
                line = line.replace("(self", "(") # remove self from first paramter
                line = re.sub(TranspileFunctionDeclarationCommand._FUNCTION_DECLARATION_SEARCH_REGEX, 
                    TranspileFunctionDeclarationCommand._FUNCTION_DECLARATION_REPLACEMENT_REGEX, line)

            output = "{}\n{}".format(output, line)
            
        return output
            