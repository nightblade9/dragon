from dragon.transpiler.lark.transformers.haxe_transformer import HaxeTransformer
from lark.lexer import Token
from lark import Tree
import unittest

class TestHaxeTransformer(unittest.TestCase):
    def test_arguments_returns_arguments(self):
        h = HaxeTransformer()
        args = [124, Tree("test", [])]
        output = h.arguments(args)
        self.assertEqual(args, output)
    
    def test_classdef_creates_non_base_class(self):
        h = HaxeTransformer()
        data = [Token("NAME", 'Monster'), [''], 'function new() { super() }']
        output = h.classdef(data)

        self.assertIn("class Monster", output)
        self.assertIn("()", output)
        self.assertIn("{", output)
        self.assertIn("}", output)

    def test_classdef_creates_subclass(self):
        h = HaxeTransformer()
        data = [Token("NAME", 'Main'), ['Sprite'], 'function new() { super().__init__()\nself.addChild(new FlxGame(0, 0, PlayState)) }']
        output = h.classdef(data)
        
        self.assertIn("class Main extends Sprite", output)
        self.assertIn("{", output)
        self.assertIn("}", output)
        self.assertIn("addChild", output)        

    def test_classdef_removes_semicolon_superclass(self):
        # Semicolon is probably a result of our semicolon-adding elsewhere
        # We should fix that first!
        h = HaxeTransformer()
        data = [Token("NAME", 'AssetPaths'), ';']
        output = h.classdef(data)
        self.assertIn("class AssetPaths", output)
        self.assertNotIn(";", output)

    def test_compound_stmt_returns_newline_separated_text(self):
        h = HaxeTransformer()
        data = ["first line", "second line", "third line!"]
        output = h.compound_stmt(data)
        self.assertEqual("\n".join(data), output)

    def test_file_input_returns_data(self):
        h = HaxeTransformer()
        x = 38
        data = ["one", x, 172.1]
        output = h.file_input(data)
        self.assertEqual(data, output)

    def test_funccall_has_brackets_when_no_parameters(self):
        h = HaxeTransformer()
        output = h.funccall(['super', Tree("arguments", [])])
        self.assertEqual("super()", output)

    def test_funccall_generates_with_parameters(self):
        h = HaxeTransformer()
        output = h.funccall(['copyInstance', Tree("arguments", ['Sprite', 'self'])])
        self.assertEqual("copyInstance(Sprite, self)", output)

    def test_funccall_specifies_target(self):
        h = HaxeTransformer()
        node = [Tree("getattr", ['super', Token("NAME", 'update')]), ['elapsed']]
        output = h.funccall(node)
        self.assertEqual("super.update(elapsed)", output)

    def test_funccall_adds_new_to_constructor(self):
        h = HaxeTransformer()
        node = ['FlxGame', [0, 0, 'PlayState']]
        output = h.funccall(node)
        self.assertEqual("new FlxGame(0, 0, PlayState)", output)

    def test_funccall_removes_args_in_constructor_call_to_super(self):
        h = HaxeTransformer()
        data = ['super', ['Sprite', 'self']]
        output = h.funccall(data)
        self.assertEqual("super()", output)

    def test_funcdef_transforms_header(self):
        h = HaxeTransformer()
        data = [Token("NAME", 'update'), ["elapsed"], 'super().update(elapsed)']
        output = h.funcdef(data)
        self.assertIn("function update(elapsed)", output)
        self.assertIn("super().update(elapsed)", output)

    def test_funcdef_transforms_init_to_new(self):
        h = HaxeTransformer()
        data = [Token("NAME", '__init__'), [], 'super().__init__()\nself.addChild(new FlxGame(0, 0, PlayState))']
        output = h.funcdef(data)
        self.assertIn("function new()", output)
        self.assertIn("addChild", output)

    def test_import_stmt_transforms_simple_imports(self):
        h = HaxeTransformer()

        node = [Tree("import_name", [Tree("dotted_as_names", [Tree("dotted_as_name",
            [Tree("dotted_name", [Token("NAME", 'PlayState')])])])])]

        output = h.import_stmt(node)
        self.assertEqual("import PlayState;", output)

    def test_import_stmt_transforms_dot_path_imports(self):
        h = HaxeTransformer()

        node = [Tree("import_from", [Tree("dotted_name", [Token("NAME", 'flixel')]),
            Tree("import_as_names", [Tree("import_as_name", [Token("NAME", 'FlxGame')])])])]

        output = h.import_stmt(node)
        self.assertEqual("import flixel.FlxGame;", output)

    def test_import_stmt_transforms_multilevel_dot_path_imports(self):
        h = HaxeTransformer()

        node = [Tree("import_from", [Tree("dotted_name", [Token("NAME", 'openfl'),
            Token("NAME", 'display')]), Tree("import_as_names", [Tree("import_as_name",
            [Token("NAME", 'Sprite')])])])]

        output = h.import_stmt(node)
        self.assertEqual("import openfl.display.Sprite;", output)
    
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

    def test_parameters_removes_first_self_param_and_returns_values_as_list(self):
        h = HaxeTransformer()
        data = [Token("NAME", 'self'), Token("NAME", 'elapsed'), Token("NAME", 'mode')]
        output = h.parameters(data)
        self.assertEqual(output, ["elapsed", "mode"])

    def test_suite_returns_newline_separated_text_with_semicolons(self):
        h = HaxeTransformer()
        data = ["first line", "second line", "third line!"]
        output = h.suite(data)
        self.assertEqual("first line;\nsecond line;\nthird line!;", output)

    def test_var_returns_variable_name(self):
        variable_names = ["Sprite", "some_variable", "out_of_100_monkeys"]
        h = HaxeTransformer()

        for token in variable_names:
            node = [Token("NAME", token)]
            output = h.var(node)
            self.assertEqual(token, output)
        