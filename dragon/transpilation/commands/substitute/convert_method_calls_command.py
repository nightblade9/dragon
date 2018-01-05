import re

class ConvertMethodCallsCommand:

    # Try to detect method calls and remove the underscores from them.  If this doesn't
    # end up being succesful, I would rather just force consumers to write "un-pythonic"
    # method calls to methods that don't have underscores in them.
    _METHOD_CALLS_SEARCH = (r"^\s*([a-zA-Z0-9_]+\.)?([a-zA-Z0-9_]+)", r"\2")

    """
    Converts imports of the form "from a.b.c import C" to "import a.b.C"
    """
    def execute(self, code):
        code = self._transform_class_declaration(code)
        return code
    
    def _transform_class_declaration(self, code):
        # TODO: what if it's just a module, not a class?
        output = code
        match = re.search(ConvertMethodCallsCommand._METHOD_CALLS_SEARCH, output)

        if (match):
            class_name = match.group(1)
            base_class = match.group(2)
            if base_class:
                base_class = base_class.replace('(', "").replace(')', "")
        
            base_class_declaration = " extends {}".format(base_class) if base_class else ""
            class_declaration = "class {}{}".format(class_name, base_class_declaration)
            
            output = output.replace(match.group(0), class_declaration)

        return output