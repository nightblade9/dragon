from dragon.generators import haxe_generator
from dragon.validators import lark_validator
from lark import Transformer
from lark import Tree
import sys

# TODO: this class is heavily coupled to Lark
# Is there a more abstract way to do this, so we can unit-test it better?
class HaxeTransformer(Transformer):

    # Arguments to a method call
    def arguments(self, node):
        arguments = node
        return haxe_generator.arguments(node)

    # Arithmethic expression
    def arith_expr(self, data):
        operand_one, operation, operand_two = data[0], data[1], data[2]
        return haxe_generator.arithmetic_expression(operation, operand_one, operand_two)

    # The "header" definition of a class (name + subclasses)
    def classdef(self, data):
        class_name = data[0].value

        # Somehow, for asset_paths.py, we get a ";" as the class path. This seems
        # like a smell that we have to properly fix; this is just a crude fix.
        base_classes = [x for x in data[1] if x != ";"]

        # throw if more than one base class
        lark_validator.validate_class_definition(class_name, base_classes)

        base_class = ""
        if len(base_classes):
            base_class = base_classes[0]
            
        class_body = ""
        # Some classes have just "pass" as the body, which we remove
        # In that case ... there is no body.
        if len(data) >= 3:
            class_body = data[2]

        return haxe_generator.class_definition(class_name, base_class, class_body)

    # A bunch of code lines thrown together.
    def compound_stmt(self, data):
        return haxe_generator.list_to_newline_separated_text(data)

    ######## prototype code
    def expr_stmt(self, data):
        return "{} = {}".format(data[0], data[1])

    def term(self, data):
        return "{} {} {}".format(data[0], data[1].value, data[2])

    ######## end prototype

    # The first node of every file.
    # This turns the output from a tree into a flat list, which is bad.
    # Alternatively, it removes the file_input line starting each file.
    def file_input(self, data):
        return data

    # Function calls; could be constructors, simple calls, calls on
    # some sort of object, etc.
    def funccall(self, node):
        # TODO: definitely break this into multiple classes/methods

        arguments = []
        
        # First parameter is a list
        if type(node[0]) == str:
            # Function call
            method_name = node[0]
            if method_name[0].isupper():
                # Constructor call
                constructor_class = node[0]
                arguments = node[1]

                return haxe_generator.method_call({"method_name": constructor_class,
                    "arguments": arguments, "is_constructor": True})
            else:
                # Method call not on an object, eg. addChild(...)
                method_name = node[0]
                arguments = _args_to_list(node[1])

                # If this is a constructor calling the base class constructor, remove
                # the parameters if the second one is "self". Typical form:
                # super(SubclassType, self).__init__(...)
                # In Haxe, this would just be "super()"
                # args to __init__ would remain as-is. That's not processed here.
                if method_name == "super" and len(arguments) == 2 and arguments[1] == "self":
                    arguments = []
                    
                return haxe_generator.method_call({"method_name": method_name,
                    "arguments": arguments})
        else:
            # Call on an object, eg. a.b(c, d)
            target = node[0].children[0]
            method_name = node[0].children[1].value

            if len(node) > 1:
                arguments = _args_to_list(node[1])           

            return haxe_generator.method_call({"method_name": method_name,
                "arguments": arguments, "target": target})
        
        return node

    # The definition of a new function
    def funcdef(self, data):
        method_name = data[0].value
        arguments = data[1] # list
        function_body = data[2]

        # methods named __init__ are mapped to new()
        return haxe_generator.method_declaration(method_name, arguments, function_body)

    def haxe(self, data):
        if isinstance(data, Tree):
            data = data.value
        elif isinstance(data, list):
            data = data[0].value
        return haxe_generator.raw_haxe(data)

    # Import statement, probably of the form: from x.a.b import B
    def import_stmt(self, node):
        node = node[0].children # import_stmt => import_from
        package_components = node[0].children

        if len(node) > 1:
            # import a.b.C
            class_name = node[1].children[0].children[0].value
        else:
            # import A
            class_name = package_components[0].children[0].children[0].value
            package_components = []

        return haxe_generator.import_statement(package_components, class_name)

    # Integer or decimal number
    def number(self, node):
        node_value = node[0].value
        return haxe_generator.number(node_value)

    # Parameters to a method call
    def parameters(self, data):
        if data[0] == "self":
            data = data[1:]
        arguments = list(map((lambda d: d.value), data))
        return haxe_generator.arguments(arguments)
    
    # There's no equivalent of this in Haxe. It's not required; empty blocks are ok.
    def pass_stmt(self, data):
        return ""

    # Long strings (""" ... """) are often our doing. We use this to support
    # Haxe features that Python doesn't have grammar support for, such as 
    # metadata (@...) or the "override" keyword on methods.
    # If it's not our custom syntax, ignore it.
    def string(self, data):
        if isinstance(data, Tree):
            data = data.value
        elif isinstance(data, list):
            data = data[0]

        return haxe_generator.string(data)

    # A bunch of code lines thrown together
    def suite(self, data):
        return haxe_generator.list_to_newline_separated_text(data, suffix_semicolons=True)

    # Simple node with a variable name
    def var(self, node):
        value = node[0].value
        return haxe_generator.value(value)

def _args_to_list(node):
    if isinstance(node, Tree):
        return node.children
    elif isinstance(node, list):
        return node
    else:
        raise NotImplementedError("Not sure how to parse {} ({}) for args".format(type(node), node))