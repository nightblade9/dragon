def number(num_string):
    if "." in num_string:
        return float(num_string)
    else:
        return int(num_string)

def import_statement(package_components, class_name):
    output = "import "
    for child_node in package_components:
        output = "{}{}.".format(output, child_node.value)

    output = "{}{}".format(output, class_name)
    return output

def value(val):
    return val