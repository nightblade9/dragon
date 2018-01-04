class AddIndentationCurlyBracesCommand:
    
    _INDENTATION_SPACES = 4 # tabs are four spaces; expect four spaces in Python.

    def execute(self, code):
        output = ""
        code_lines = code.splitlines()
        for index, line in enumerate(code_lines):
            next_line = code_lines[index + 1] if index < len(code_lines) - 1 else ""
            # Convert tabs into spaces so we count uniformly
            my_indentation_level = self._get_indentation_level(line)
            next_indentation_level = self._get_indentation_level(next_line)
            print("({}) {}".format(my_indentation_level, line))

            add_character = ""
            if my_indentation_level > next_indentation_level:
                # Completed a block
                add_character = " }"
            elif my_indentation_level < next_indentation_level:
                # Started a new block
                add_character = " {"
            
            output = "{}\n{}{}".format(output, line, add_character)

        # Add a final closing-brace. Because, ya know, it's assumed to be a class.
        output = "{}\n}}".format(output)
        return output

    def _get_indentation_level(self, line):
        space_normalized_line = line.replace("\t", "    ")
        leading_spaces_count = len(space_normalized_line) - len(space_normalized_line.lstrip(' '))
        return leading_spaces_count / AddIndentationCurlyBracesCommand._INDENTATION_SPACES
