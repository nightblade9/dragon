from dragon.generators import haxe_generator
from lark.lexer import Token
from lark import Tree
import unittest

class TestHaxeGenerator(unittest.TestCase):
    def test_arguments_returns_arguments(self):
        args = [124, Tree("test", [])]
        output = haxe_generator.arguments(args)
        self.assertEqual(args, output)

    def test_arguments_quotes_strings(self):
        output = haxe_generator.arguments(['a', 'b'])
        self.assertEqual(output, ['a', 'b'])

    def test_import_statement_transforms_simple_imports(self):
        output = haxe_generator.import_statement([], "PlayState")
        self.assertEqual("import PlayState", output)

    def test_import_statement_transforms_dot_path_imports(self):
        output = haxe_generator.import_statement(["flixel"], "FlxGame")
        self.assertEqual("import flixel.FlxGame", output)

    def test_import_statement_transforms_multilevel_dot_path_imports(self):
        output = haxe_generator.import_statement(["openfl", "display"], "Sprite")
        self.assertEqual("import openfl.display.Sprite", output)
    
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
