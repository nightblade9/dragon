import re

"""
Rules on what regex to apply as a search/replace operation.
"""
# Dumb data class; allows us to have named rules.
class LineSubstitutionRule:
    def __init__(self, search, replacement):
        self.search = search
        self.replacement = replacement

def apply(rule, text):
    text_lines = text.splitlines()
    output = ""

    for line in text_lines:
        line = re.sub(rule.search, rule.replacement, line)
        output = "{}\n{}".format(output, line)
        
    return output
