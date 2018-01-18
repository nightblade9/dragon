#!/usr/bin/env python3
# TODO: move into Mars project
import glob
import os
import sys

from dragon.transpiler.python_to_haxe_transpiler import PythonToHaxeTranspiler
from dragon.template_creator import TemplateCreator

TEMPLATE_COMMAND = "template"
BUILD_COMMAND = "build"
VALID_COMMANDS = (TEMPLATE_COMMAND, BUILD_COMMAND)

def mars(args):
    if len(args) >= 1:
        command = args[0]
        if command == TEMPLATE_COMMAND:
            if len(args) >= 2:
                template_creator = TemplateCreator(args[1])
            else:
                template_creator = TemplateCreator()
            template_creator.create_template()
            print("Template project created in {}".format(template_creator.output_directory))
        elif command == BUILD_COMMAND:
            if len(args) >= 2:
                source_path = args[1]
                files_path = os.path.join(os.getcwd(), source_path, "**/*.py")
                files = glob.glob(files_path, recursive=True)
                print("Transpiling {} files...".format(len(files)))
                PythonToHaxeTranspiler(source_path, files).transpile()
            else:
                print("Please specify the target directory to build.")
        else:
            print("'{}' is not a valid command. Valid commands are: {}".format(command, VALID_COMMANDS))
    else:
        print("Usage: python main.py {}".format(VALID_COMMANDS))

if __name__ == "__main__":
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    mars(args)