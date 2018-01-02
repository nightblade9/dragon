from dragon.template_creator import TemplateCreator
import os
import shutil
import unittest

class TestTemplateCreator(unittest.TestCase):

    GENERATED_TEMPLATE_DIR = "delme"
    # assets dir, source dir, Project.xml
    EXPECTED_HAXEFLIXEL_FILES = ["assets", "Project.xml", "source"]
    
    def tearDown(self):
        if os.path.exists(TestTemplateCreator.GENERATED_TEMPLATE_DIR):
            shutil.rmtree(TestTemplateCreator.GENERATED_TEMPLATE_DIR)

    def test_initializer_sets_output_directory_to_parameter_value(self):
        t = TemplateCreator(None)
        self.assertIsNotNone(t.output_directory)

        t = TemplateCreator("hi")
        self.assertIn("hi", t.output_directory)

    def test_create_template_creates_templates(self):
        t = TemplateCreator(TestTemplateCreator.GENERATED_TEMPLATE_DIR)
        t.create_template()
        self.assertTrue(os.path.exists(TestTemplateCreator.GENERATED_TEMPLATE_DIR))
        self.assertTrue(os.path.isdir(TestTemplateCreator.GENERATED_TEMPLATE_DIR))

        files_and_directories = os.listdir(TestTemplateCreator.GENERATED_TEMPLATE_DIR)
        self.assertGreaterEqual(len(files_and_directories), len(TestTemplateCreator.EXPECTED_HAXEFLIXEL_FILES))
        # Qualitative check: no files, and at least Project.xml, source, assets
        for entry in TestTemplateCreator.EXPECTED_HAXEFLIXEL_FILES:
            self.assertTrue(os.path.exists(os.path.join(TestTemplateCreator.GENERATED_TEMPLATE_DIR, entry)))
