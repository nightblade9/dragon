from dragon.generators import haxe_generator
from lark.lexer import Token
from lark import Tree
import unittest

class TestHaxeGenerator(unittest.TestCase):
    def test_number_transforms_decimal_numbers_to_floats(self):
        for num in (0.0, 17.021, -183.123456):
            output = haxe_generator.number("{}".format(num))
            self.assertEqual(num, output)

    def test_number_transforms_integer_numbers_to_floats(self):
        for num in (0, 9999, -19232):
            output = haxe_generator.number("{}".format(num))
            self.assertEqual(num, output)

    def test_var_returns_variable_name(self):
        variable_names = ["Sprite", "some_variable", "out_of_100_monkeys"]

        for token in variable_names:
            output = haxe_generator.value(token)
            self.assertEqual(token, output)