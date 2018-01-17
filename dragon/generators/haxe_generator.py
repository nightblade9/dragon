_METADATA_START = '"""@'
_METADATA_END = '"""'
_OVERRIDE_SYNTAX = '"""#override"""'
_OVERRIDE_GENERATED = "override"

def arguments(args):
    return [v for v in args]

def class_definition(class_name, base_class, class_body):
    return "class {}{} {{\n{}\n}}".format(
        class_name,
        "" if base_class == "" else " extends {}".format(base_class),
        class_body)

def import_statement(package_components, class_name):
    output = "import "
    for component in package_components:
        output = "{}{}.".format(output, component)

    output = "{}{};".format(output, class_name)
    return output

def list_to_newline_separated_text(data, suffix_semicolons=False):
    if suffix_semicolons:
        to_return = []
        for line in data:
            if "{" not in line and "}" not in line and line != _OVERRIDE_GENERATED:
                line = "{};".format(line)
            to_return.append(line)
        data = to_return

    return "\n".join(data)

# Method calls. TODO: extract into a different class?
def method_call(data):
    method_name = data["method_name"]

    if "is_constructor" in data and data["is_constructor"]:
        method_name = "new {}".format(method_name)
    
    raw_arguments = data["arguments"]
    args = []
    for arg in raw_arguments:
        args.append("{}".format(arg)) # to_string
    
    target = ""
    if "target" in data:
        target = data["target"]
        if (target == "super" or target == "super()") and method_name == "__init__":
            return "super({})".format(", ".join(args))
        else:
            target = "{}.".format(target)

    output = "{}{}({})".format(target, method_name, ", ".join(args))
    return output

def custom_token_or_long_string(data):
    if data.startswith(_METADATA_START) and data.endswith(_METADATA_END):
        start = data.index(_METADATA_START) + len(_METADATA_START) - 1
        stop = data.rindex(_METADATA_END)
        to_return = data[start:stop]
        return to_return
    elif data == _OVERRIDE_SYNTAX:
        return _OVERRIDE_GENERATED
    else:
        # To paraphrase Python's benevolant dictator: these are 
        # block comments, they don't generate into code!
        return ""

def method_declaration(method_name, args, method_body):
    if method_name == "__init__":
        method_name = "new" 
    
    return "function {}({}) {{\n{}\n}}".format(method_name, ",".join(args), method_body)

def number(num_string):
    if "." in num_string:
        return float(num_string)
    else:
        return int(num_string)

def value(val):
    return val