from lark import Transformer
import sys

# TODO: this class is heavily coupled to Lark
# Is there a more abstract way to do this, so we can unit-test it better?
class HaxeTransformer(Transformer):

    DEBUG_NODE = None

    # Transform from "x.a.b import B" (or "C") to "import x.a.b.B" or "import x.a.b.C"
    def import_stmt(self, node):
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
        return float(node[0].value)