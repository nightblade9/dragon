def arguments(args):
    return [v for v in args]

def class_definition(class_name, base_class, class_body):
    return "class {}{} {{ {} }}".format(
        class_name,
        "" if base_class == "" else " extends {}".format(base_class),
        class_body)

def import_statement(package_components, class_name):
    output = "import "
    for component in package_components:
        output = "{}{}.".format(output, component)

    output = "{}{};".format(output, class_name)
    return output

def list_to_newline_separated_text(data):
    return "\n".join(data)

# Method calls. TODO: extract into a different class?
def method_call(data):
    method_name = data["method_name"]

    if "is_constructor" in data and data["is_constructor"]:
        method_name = "new {}".format(method_name)

    raw_arguments = data["arguments"]
    arguments = []
    for arg in raw_arguments:
        arguments.append("{}".format(arg)) # to_string
    
    target = ""
    if "target" in data:
        target = "{}.".format(data["target"])

    output = "{}{}({})".format(target, method_name, ", ".join(arguments))
    return output

def method_declaration(method_name, arguments, method_body):
    return "function {}({}) {{ {} }}".format(method_name, ",".join(arguments), method_body)

def number(num_string):
    if "." in num_string:
        return float(num_string)
    else:
        return int(num_string)

def value(val):
    return val