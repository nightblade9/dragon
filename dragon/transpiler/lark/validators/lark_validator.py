from lark import Tree
import re

class LarkValidator:
    
    _TOKEN_REGEX = r"^([a-zA-Z0-9_\-\?!_\.]+):"

    def __init__(self, grammar_filename):
        self._grammar_tokens = self._extract_tokens(grammar_filename)

    def is_fully_parsed(self, code):
        for line in code:
            for token in self._grammar_tokens:
                if token in line:
                    print("Found unparsed token {} in line {}".format(token, line))
                    return False
            
        return True
             
    def _extract_tokens(self, grammar_filename):
        with open(grammar_filename, "rt") as f:
            grammar = f.read()

        lines = grammar.splitlines()
        tokens = []

        for line in lines:
            match = re.search(LarkValidator._TOKEN_REGEX, line)
            if match:
                token = match.group(1)                
                token_name = token.replace("?", "").replace("!", "")
                tokens.append(token_name)
        
        return tokens
                

def validate_class_definition(class_name, base_classes):
    if len(base_classes) > 1:
        raise ValueError("Class {} should not have more than one base class: {}".format(class_name, base_classes))
