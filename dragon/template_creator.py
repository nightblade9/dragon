import os
import sys
import shutil

# TODO: move into Mars project
class TemplateCreator:

    DEFAULT_OUTPUT_DIRECTORY = 'template' # directory to be created
    SOURCE_TEMPLATE_DIRECTORY = 'template'

    def __init__(self, output_directory_name = None):
        if output_directory_name:
            self.output_directory = output_directory_name
        else:
            self.output_directory = TemplateCreator.DEFAULT_OUTPUT_DIRECTORY
        
        dragon_path = os.path.dirname(os.path.realpath(__file__))
        dragon_path = os.path.split(dragon_path)[0] # Windows only?
        self._source_directory = os.path.join(dragon_path, TemplateCreator.SOURCE_TEMPLATE_DIRECTORY)

    def create_template(self):
        try:
            print("Creating template project in directory {}...".format(self.output_directory))
            shutil.copytree(self._source_directory, self.output_directory)
        except Exception:
            print("Couldn't create the template directory; is there already a directory named '{}'?".format(self.output_directory))
            raise