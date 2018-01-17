import os

def add_package_statement(source_root, path_and_filename, code, path_separator=os.path.sep):
    # eg. source_root = template\source, filename = template\source\main.py
    # Resulting package should be empty string. Subtract the two strings.
    filename = path_and_filename[0:path_and_filename.rindex(path_separator)]
    filename = filename.replace(source_root, "")
    # Sometimes the first character is a path separator that we don't want
    filename = filename[1:] if len(filename) and filename[0] == path_separator else filename
    package = filename.replace(path_separator, ".")
    code = "package {};\n{}".format(package, "\n".join(code))
    return code

def camel_case_to_pep8_method_name(name):
    output = name[0]
    for i in range(1, len(name)):
        # Note: !upper() covers symbols, numbers, etc. lower() doesn't.
        if name[i].isupper() and not name[i - 1].isupper():
            output = "{}_{}".format(output, name[i])
        else:
            output = "{}{}".format(output, name[i])
    
    output = output.replace("__", "_")
    return output.lower()
