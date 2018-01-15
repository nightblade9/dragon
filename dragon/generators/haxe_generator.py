def arguments(args):
    return [v for v in args]

def import_statement(package_components, class_name):
    output = "import "
    for component in package_components:
        output = "{}{}.".format(output, component)

    output = "{}{};".format(output, class_name)
    return output

def number(num_string):
    if "." in num_string:
        return float(num_string)
    else:
        return int(num_string)

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

def value(val):
    return val