from dragon.transpiler.lark.transformers.haxe_transformer import HaxeTransformer
from lark.lexer import Token
from lark import Tree
import unittest

class TestHaxeTransformer(unittest.TestCase):
    def test_import_stmt_transforms_simple_imports(self):
        h = HaxeTransformer()

        node = [Tree("import_name", [Tree("dotted_as_names", [Tree("dotted_as_name",
            [Tree("dotted_name", [Token("NAME", 'PlayState')])])])])]

        output = h.import_stmt(node)
        self.assertEqual("import PlayState", output)

    def test_import_stmt_transforms_dot_path_imports(self):
        h = HaxeTransformer()

        node = [Tree("import_from", [Tree("dotted_name", [Token("NAME", 'flixel')]),
            Tree("import_as_names", [Tree("import_as_name", [Token("NAME", 'FlxGame')])])])]

        output = h.import_stmt(node)
        self.assertEqual("import flixel.FlxGame", output)

    def test_import_stmt_transforms_multilevel_dot_path_imports(self):
        h = HaxeTransformer()

        node = [Tree("import_from", [Tree("dotted_name", [Token("NAME", 'openfl'),
            Token("NAME", 'display')]), Tree("import_as_names", [Tree("import_as_name",
            [Token("NAME", 'Sprite')])])])]

        output = h.import_stmt(node)
        self.assertEqual("import openfl.display.Sprite", output)

    def test_number_transforms_decimal_numbers_to_floats(self):
        for num in (0.0, 17.021, -183.123456):
            h = HaxeTransformer()
            node = [Token("DEC_NUMBER", '{}'.format(num))]
            output = h.number(node)
            self.assertEqual(num, output)

    def test_number_transforms_integer_numbers_to_floats(self):
        h = HaxeTransformer()
        for num in (0, 9999, -19232):
            node = [Token("DEC_NUMBER", '{}'.format(num))]
            output = h.number(node)
            self.assertEqual(num, output)

    def test_var_returns_variable_name(self):
        variable_names = ["Sprite", "some_variable", "out_of_100_monkeys"]
        h = HaxeTransformer()

        for token in variable_names:
            node = [Token("NAME", token)]
            output = h.var(node)
            self.assertEqual(token, output)
        
    def test_method_call_has_brackets_when_no_parameters(self):
        h = HaxeTransformer()
        output = h.funccall(['super', Tree("arguments", [])])
        self.assertEqual("super()", output)

    def test_method_call_generates_with_parameters(self):
        h = HaxeTransformer()
        output = h.funccall(['copyInstance', Tree("arguments", ['Sprite', 'self'])])
        self.assertEqual("copyInstance(Sprite, self)", output)
