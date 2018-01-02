from dragon.template_creator import TemplateCreator
import os
import shutil
import unittest

class TestTemplateCreator(unittest.TestCase):
    GENERATED_TEMPLATE_DIR = "delme"
    
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