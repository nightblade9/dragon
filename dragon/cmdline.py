#!/usr/bin/env python3
import sys

from template_creator import TemplateCreator

def main():
    commandline_args = sys.argv
    if len(commandline_args) > 1:
        command = commandline_args[1]
        if command == "create":
            template_creator = TemplateCreator()
            template_creator.create_template()
            print("Template project created in {}".format(template_creator.template_directory))
        else:
            print("'{}' is not a valid command. Valid commands are: create".format(command))
    else:
        print("Usage: python cmdline.py create")

if __name__ == "__main__":
    main()