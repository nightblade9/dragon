from dragon.generators import haxe_generator
from dragon.transpiler.lark.validators import lark_validator
from lark import Transformer
from lark import Tree
import sys

# TODO: this class is heavily coupled to Lark
# Is there a more abstract way to do this, so we can unit-test it better?
class HaxeTransformer(Transformer):

    DEBUG_NODE = None

    def arguments(self, node):
        arguments = node
        return haxe_generator.arguments(node)

    def classdef(self, data):
        class_name = data[0].value
        base_classes = data[1]

        # throw if more than one base class
        lark_validator.validate_class_definition(class_name, base_classes)

        base_class = base_classes[0]
        class_body = data[2]

        return haxe_generator.class_definition(class_name, base_class, class_body)

    def compound_stmt(self, data):
        print("COMP {}".format(data))
        return "\n".join(data)

    def funccall(self, node):
        # TODO: definitely break this into multiple classes/methods

        HaxeTransformer.DEBUG_NODE = node
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

    def funcdef(self, data):
        method_name = data[0].value
        arguments = data[1] # list
        function_body = data[2]

        # methods named __init__ are mapped to new()
        method_name = "new" if method_name == "__init__" else method_name
        return haxe_generator.method_declaration(method_name, arguments, function_body)

    def import_stmt(self, node):
        # Import statement, probably of the form: from x.a.b import B
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

    def number(self, node):
        # Integer or decimal number
        HaxeTransformer.DEBUG_NODE = node
        node_value = node[0].value
        return haxe_generator.number(node_value)

    def parameters(self, data):
        if data[0] == "self":
            data = data[1:]
        arguments = list(map((lambda d: d.value), data))
        return haxe_generator.arguments(arguments)

    def suite(self, data):
        print("SUITE: {}".format(data))
        return "\n".join(data)

    def var(self, node):
        # Simple node with a variable name
        value = node[0].value
        return haxe_generator.value(value)

def _args_to_list(node):
    if isinstance(node, Tree):
        return node.children
    elif isinstance(node, list):
        return node
    else:
        raise NotImplementedError("Not sure how to parse {} ({}) for args".format(type(node), node))