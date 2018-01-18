#!/usr/bin/env python3
# TODO: move into Mars project
import glob
import os
import sys

from dragon.transpiler.python_to_haxe_transpiler import PythonToHaxeTranspiler
from dragon.template_creator import TemplateCreator

TEMPLATE_COMMAND = "template"
VALID_COMMANDS = [TEMPLATE_COMMAND]

def dragon(args):
    # Debug mode!
    if len(args) == 0:
        # Just transpile in-place for now.
        source_path = os.path.join("template", "source")
        files = glob.glob(os.path.join(source_path, "**/*.py"))
        PythonToHaxeTranspiler(source_path, files).transpile()
    elif len(args) >= 1:
        command = args[0]
        if command == TEMPLATE_COMMAND:
            if len(args) >= 2:
                template_creator = TemplateCreator(args[1])
            else:
                template_creator = TemplateCreator()
            template_creator.create_template()
            print("Template project created in {}".format(template_creator.output_directory))
        else:
            print("'{}' is not a valid command. Valid commands are: {}".format(command, VALID_COMMANDS))
    else:
        print("Usage: python cmdline.py {}".format(VALID_COMMANDS))

if __name__ == "__main__":
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    dragon(args)