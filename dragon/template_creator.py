import sys
import shutil

class TemplateCreator:

    DEFAULT_OUTPUT_DIRECTORY = 'template' # directory to be created
    SOURCE_TEMPLATE_DIRECTORY = 'template'

    def __init__(self, directory_name = None):
        if directory_name:
            self.output_directory = directory_name
        else:
            self.output_directory = TemplateCreator.DEFAULT_OUTPUT_DIRECTORY

        self.source_directory = "{}\\{}".format(sys.path[0], TemplateCreator.SOURCE_TEMPLATE_DIRECTORY)

    def create_template(self):
        try:
            print("Copying from {} tp {}".format(self.source_directory, self.output_directory))
            shutil.copytree(self.source_directory, self.output_directory)
        except Exception:
            print("Couldn't create the template directory; is there already a directory named '{}'?".format(self.output_directory))
            raise