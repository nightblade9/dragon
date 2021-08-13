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

            add_character = ""
            if my_indentation_level > next_indentation_level:
                # Completed one or more blocks
                for n in range(my_indentation_level - next_indentation_level):
                    num_levels = my_indentation_level - n - 1
                    spaces = num_levels * AddIndentationCurlyBracesCommand._INDENTATION_SPACES * " "
                    add_character = "{}\n{}}}".format(add_character, spaces)
            elif my_indentation_level < next_indentation_level:
                # Started a new block
                add_character = " {"
            
            output = "{}\n{}{}".format(output, line, add_character)

        return output

    def _get_indentation_level(self, line):
        space_normalized_line = line.replace("\t", "    ")
        leading_spaces_count = len(space_normalized_line) - len(space_normalized_line.lstrip(' '))
        return leading_spaces_count // AddIndentationCurlyBracesCommand._INDENTATION_SPACES
