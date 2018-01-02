import os

class TemplateCreator:

    DEFAULT_DIRECTORY_NAME = 'template'

    def __init__(self):
        self.template_directory = TemplateCreator.DEFAULT_DIRECTORY_NAME

    def create_template(self):
        try:
            os.mkdir(self.template_directory)
        except:
            print("Couldn't create the template directory; is there already a directory named '{}'?".format(self.template_directory))

    def template_directory(self):
        return TemplateCreator.DEFAULT_DIRECTORY_NAME