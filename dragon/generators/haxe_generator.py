def number(num_string):
    if "." in num_string:
        return float(num_string)
    else:
        return int(num_string)

def import_statement(package_components, class_name):
    output = "import "
    for component in package_components:
        output = "{}{}.".format(output, component)

    output = "{}{}".format(output, class_name)
    return output

# Method calls. TODO: extract into a different class?
def method_call(method_name, arguments):
    output = "{}({})".format(method_name, ", ".join(arguments))
    return output

def value(val):
    return val