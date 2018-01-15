from lark import Tree
import re

class LarkValidator:
    
    _TOKEN_REGEX = r"^([a-zA-Z0-9_\-]+):"

    def __init__(self, grammar_filename):
        self._grammar_tokens = self._extract_tokens(grammar_filename)

    def is_fully_parsed(self, tree):
        if isinstance(tree, str) and tree in self._tokens:
            print("Found an unprocessed token: {}".format(tree))
            return False
        elif isinstance(tree, Tree):
            if tree.data in self._tokens:
                print("Found an unprocessed subtree: {}".format(tree.data))
                return False
            if len(tree.children):
                for node in tree.children:
                    if not self.is_fully_parsed(node):
                        print("Found an unprocessed node: {}".format(node.data))
                        return False
        
        return True
             
    def _extract_tokens(self, grammar_filename):
        with open(grammar_filename, "rt") as f:
            grammar = f.read()

        lines = grammar.splitlines()
        self._tokens = []

        for line in lines:
            match = re.search(LarkValidator._TOKEN_REGEX, line)
            if match:
                token = match.group(1)
                self._tokens.append(token)

def validate_class_definition(class_name, base_classes):
    if len(base_classes) > 1:
        raise ValueError("Class {} should not have more than one base class: {}".format(class_name, base_classes))
