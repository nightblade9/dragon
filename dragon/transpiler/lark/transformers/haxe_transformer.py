from lark import Transformer
import sys

# TODO: this class is heavily coupled to Lark
# Is there a more abstract way to do this, so we can unit-test it better?
class HaxeTransformer(Transformer):

    DEBUG_NODE = None

    def funccall(self, node):
        # TODO: definitely break this into multiple classes/methods

        HaxeTransformer.DEBUG_NODE = node
        

    def import_stmt(self, node):
        # Import statement, probably of the form: from x.a.b import B
        output = "import "
        
        node = node[0].children # import_stmt => import_from
        package_name = node[0].children

        if len(node) > 1:
            # import a.b.C
            for child_node in package_name:
                output = "{}{}.".format(output, child_node.value)

            class_name = node[1].children[0].children[0].value
            output = "{}{}".format(output, class_name)
        else:
            # import A
            output = "{}{}".format(output, package_name[0].children[0].children[0].value)

        return output

    def number(self, node):
        # Integer or decimal number
        HaxeTransformer.DEBUG_NODE = node
        node_value = node[0].value

        if "." in node_value:
            return float(node_value)
        else:
            return int(node_value)

    def var(self, node):
        # Simple node with a variable name
        value = node[0].value
        return value
