import re

# Not just the "def", but also removes arguments ... including "self"
FUNCTION_DECLARATION_RULE = (r"def ([a-zA-Z0-9_]+)(\([a-zA-Z0-9_, ]+\))?:", r"function \1()")

# We only support newstyle "from x import y". Applied line by line.
# The second grouping [a-zA-Z_] removes the final redundancy from the import
# eg. "from openfl.display.sprite import Sprite" ignores ".sprite"
IMPORT_STATEMENT_RULE = (r"^from ([a-zA-Z\._]+)\.[a-zA-Z_]+ import ([a-zA-Z_]+)", r"import \1.\2;")

def apply_regex(rule_tuple, text):
    text_lines = text.splitlines()
    output = ""

    for line in text_lines:
        search = rule_tuple[0]
        replacement = rule_tuple[1]
        line = re.sub(search, replacement, line)
        output = "{}\n{}".format(output, line)
        
    return output