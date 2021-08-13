from dragon.generators import haxe_generator
from lark.lexer import Token
from lark import Tree
from nose_parameterized import parameterized
import unittest

class TestHaxeGenerator(unittest.TestCase):

    @parameterized.expand([
        [-212, "+", 2124],
        [34, "-", 21.014],
        [-1.07776, "*", -156],
        [0, "/", 0]
    ])

    def test_arithmetic_expression_adds_brackets(self, operand_one, operation, operand_two):
        output = haxe_generator.arithmetic_expression([operand_one, operation, operand_two])
        self.assertEqual("({} {} {})".format(operand_one, operation, operand_two), output)

    def test_arithmetic_expression_satisfies_bedmas(self):
        input = [17, "+", 'm * x', "+", 'b']
        actual = haxe_generator.arithmetic_expression(input)
        expected = "(((17 + (m * x))) + b)" # death by brackets, but BEDMAS is preserved
        self.assertEqual(expected, actual)

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

    def test_list_to_newline_separated_text_generates_text_with_newlines_and_semicolons(self):
        data = ["first line", "second line", "third line!"]
        output = haxe_generator.list_to_newline_separated_text(data, suffix_semicolons=True)
        self.assertEqual("first line;\nsecond line;\nthird line!;", output)
        self.assertEqual(len(data), output.count(";"))

    def test_list_to_newline_excludes_override_statements(self):
        data = ["class X extends FlxState", "override", "public function create()"]
        output = haxe_generator.list_to_newline_separated_text(data, suffix_semicolons=True)
        self.assertEqual("class X extends FlxState;\noverride\npublic function create();", output)

    def test_string_turns_docstring_into_empty_string(self):
        data = '"""Here is a nice doc-string comment!"""'
        output = haxe_generator.string(data)
        self.assertEqual("", output)

    @parameterized.expand([
        ['super()'], # method call
        ['just a regular string'],
        ['$p#$CiaL_*""()'], # special characters
        ['123.456'], # float
        ["And here's a long string with a bunch of unnecessary characters."]
    ])
    def test_string_leaves_strings_intact(self, data):
        output = haxe_generator.string(data)
        self.assertEqual(data, output)

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

    def test_method_call_changes_target_from_self_to_this(self):
        output = haxe_generator.method_call({"method_name": "fight", "arguments": ["monster"],
            "target": "self"})
        self.assertEqual("this.fight(monster)", output)

    def test_method_call_generates_constructor_when_is_constructor_is_true(self):
        output = haxe_generator.method_call({"method_name": "Monster", "arguments": ['"assets/images/duck.png"', 5, 1],
            "is_constructor": True})

        self.assertEqual('new Monster("assets/images/duck.png", 5, 1)', output)
    
    @parameterized.expand([
        ['super()'],
        ['super']
    ])
    def test_method_call_generates_constructor_when_method_name_is_init_and_target_is_super(self, target):
        data = {'method_name': '__init__', 'arguments': [], 'target': target}
        output = haxe_generator.method_call(data)
        self.assertEqual("super()", output)

    def test_method_call_turns_super_call_to_init_into_regular_super_call(self):
        output = haxe_generator.method_call({"target": "super", "method_name": "__init__", "arguments": ["x", "y"]})
        self.assertEqual("super(x, y)", output)

    def test_method_call_converts_print_to_trace(self):
        output = haxe_generator.method_call({"method_name": "print", "arguments": ['"Hello from Python!"']})
        self.assertEqual("trace(\"Hello from Python!\")", output)


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

    def test_raw_haxe_extracts_haxe_code(self):
        haxe_code = "a.b(c, d)"
        output= haxe_generator.raw_haxe("@haxe: {}".format(haxe_code))
        self.assertEqual(haxe_code, output)

    def test_value_returns_variable_name(self):
        variable_names = ["Sprite", "some_variable", "out_of_100_monkeys"]

        for token in variable_names:
            output = haxe_generator.value(token)
            self.assertEqual(token, output)
