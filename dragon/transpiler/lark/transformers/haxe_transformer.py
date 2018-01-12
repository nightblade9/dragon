from dragon.generators import haxe_generator
from lark import Transformer
import sys

# TODO: this class is heavily coupled to Lark
# Is there a more abstract way to do this, so we can unit-test it better?
class HaxeTransformer(Transformer):

    DEBUG_NODE = None

    def funccall(self, node):
        # TODO: definitely break this into multiple classes/methods

        HaxeTransformer.DEBUG_NODE = node
        # First parameter is a list
        if type(node[0]) == str:
            # Function call
            method_name = node[0]
            if method_name[0].isupper():
                # Constructor call
                print("constructor: {}".format(node))
            else:
                # Method call not on an object, eg. addChild(...)
                method = node[0]
                arguments = node[1].children
                return haxe_generator.method_call(method, arguments)
        else:
            # I have no idea what to do here.
            print("call on an obj: {}".format(node))
        
        return node

    def import_stmt(self, node):
        # Import statement, probably of the form: from x.a.b import B
        output = "import "
        
        node = node[0].children # import_stmt => import_from
        package_components = node[0].children

        if len(node) > 1:
            # import a.b.C
            class_name = node[1].children[0].children[0].value
            output = "{}{}".format(output, class_name)
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

    def var(self, node):
        # Simple node with a variable name
        value = node[0].value
        return haxe_generator.value(value)
