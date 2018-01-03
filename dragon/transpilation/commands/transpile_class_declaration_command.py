import re

class TranspileClassDeclarationCommand:

    _CLASS_SEARCH_REGEX = r"class ([a-zA-Z]+)(\([a-zA-Z]+\))?:"
    _CLASS_REPLACEMENT_REGEX = r""

    """
    Converts imports of the form "from a.b.c import C" to "import a.b.C"
    """
    def execute(self, code):
        code = self._transform_class_declaration(code)
        return code
    
    def _transform_class_declaration(self, code):
        # TODO: what if it's just a module, not a class?
        output = code
        match = re.search(TranspileClassDeclarationCommand._CLASS_SEARCH_REGEX, output)

        if (match):
            class_name = match.group(1)
            base_class = match.group(2)
            if base_class:
                base_class = base_class.replace('(', "").replace(')', "")
        
            base_class_declaration = " extends {}".format(base_class) if base_class else ""
            class_declaration = "class {}{} {{".format(class_name, base_class_declaration)
            
            output = output.replace(match.group(0), class_declaration)

        return output