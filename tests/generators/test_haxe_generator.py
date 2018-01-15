from dragon.generators import haxe_generator
from lark.lexer import Token
from lark import Tree
import unittest

class TestHaxeGenerator(unittest.TestCase):
    def test_arguments_returns_arguments(self):
        args = [124, Tree("test", [])]
        output = haxe_generator.arguments(args)
        self.assertEqual(args, output)

    def test_class_definition_creates_non_base_class(self):
        output = haxe_generator.class_definition("Monster", "", "")
        self.assertIn("class Monster", output)
        self.assertIn("{", output)
        self.assertIn("}", output)

    def test_class_definition_creates_subclass(self):
        output = haxe_generator.class_definition("Monster", "HelixSprite", "")
        self.assertIn("class Monster extends HelixSprite", output)
        self.assertIn("{", output)
        self.assertIn("}", output)

    def test_import_statement_transforms_simple_imports(self):
        output = haxe_generator.import_statement([], "PlayState")
        self.assertEqual("import PlayState;", output)

    def test_import_statement_transforms_dot_path_imports(self):
        output = haxe_generator.import_statement(["flixel"], "FlxGame")
        self.assertEqual("import flixel.FlxGame;", output)

    def test_import_statement_transforms_multilevel_dot_path_imports(self):
        output = haxe_generator.import_statement(["openfl", "display"], "Sprite")
        self.assertEqual("import openfl.display.Sprite;", output)
    
    def test_list_to_newline_separated_text_generates_text_with_newlines(self):
        data = ["first line", "second line", "third line!"]
        output = haxe_generator.list_to_newline_separated_text(data)
        self.assertEqual("\n".join(data), output)
        self.assertNotIn(";", output)

    def test_list_to_newline_separated_text_generates_text_with_newlines(self):
        data = ["first line", "second line", "third line!"]
        output = haxe_generator.list_to_newline_separated_text(data, suffix_semicolons=True)
        self.assertEqual("first line;\nsecond line;\nthird line!;", output)
        self.assertEqual(len(data), output.count(";"))

    def test_method_call_has_brackets_when_no_parameters(self):
        output = haxe_generator.method_call({"method_name": "destroy", "arguments": []})
        self.assertEqual("destroy()", output)

    def test_method_call_generates_with_parameters(self):
        output = haxe_generator.method_call({"method_name": "calculateDistance",
            "arguments": ["x1", "x2", "player.y", "377"]})
        self.assertEqual("calculateDistance(x1, x2, player.y, 377)", output)

    def test_method_call_specifies_target(self):
        output = haxe_generator.method_call({"method_name": "damage", "arguments": [28],
            "target": "monster"})
        self.assertEqual("monster.damage(28)", output)

    def test_method_call_generates_constructor(self):
        output = haxe_generator.method_call({"method_name": "Monster", "arguments": ['"assets/images/duck.png"', 5, 1],
            "is_constructor": True})

        self.assertEqual('new Monster("assets/images/duck.png", 5, 1)', output)

    def test_method_declaration_renames_init_to_new(self):
        output = haxe_generator.method_declaration("__init__", [], "super()")
        self.assertIn("function new()", output)
        self.assertIn("super()", output)

    def test_method_declaration_renames_init_to_new_and_passes_parameters(self):
        output = haxe_generator.method_declaration("__init__", ["level"], "super(level)")
        self.assertIn("function new(level)", output)
        self.assertIn("super(level)", output)

    def test_method_declaration_generates_header(self):
        output = haxe_generator.method_declaration("gameOver", [], "self.destroy()")
        self.assertIn("function gameOver()", output)
        self.assertIn(".destroy", output)

    def test_method_declaration_generates_header_with_parameters(self):
        output = haxe_generator.method_declaration("damage", ["amount"], "this.amount -= health")
        self.assertIn("function damage(amount)", output)
        self.assertIn("this.amount -= health", output)

    def test_number_transforms_decimal_numbers_to_floats(self):
        for num in (0.0, 17.021, -183.123456):
            output = haxe_generator.number("{}".format(num))
            self.assertEqual(num, output)

    def test_number_transforms_integer_numbers_to_floats(self):
        for num in (0, 9999, -19232):
            output = haxe_generator.number("{}".format(num))
            self.assertEqual(num, output)

    def test_value_returns_variable_name(self):
        variable_names = ["Sprite", "some_variable", "out_of_100_monkeys"]

        for token in variable_names:
            output = haxe_generator.value(token)
            self.assertEqual(token, output)
