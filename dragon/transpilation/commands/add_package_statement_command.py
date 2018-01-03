import os

class AddPackageStatementCommand:

    """
    Adds a "package a.b.c;" statement depending on the file path.
    """
    def execute(self, filename, code):
        path_only = os.path.split(filename)[0]
        packages = path_only.split(os.path.sep)
        package_statement = "package"

        if len(packages) and packages != [""]:
            package_statement = "package {}".format(".".join(packages))

        package_statement = "{};".format(package_statement)
        code = "{}\n{}".format(package_statement, code)
        return code
