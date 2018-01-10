class RemoveBlankLinesCommand:
    """
    Removes blank lines. Makes it easier to add curly-braces properly.
    """
    def execute(code):
        output = ""
        lines = code.splitlines()

        for line in lines:
            if len(line.strip()):
                output = "{}\n{}".format(output, line)

        return output.strip()