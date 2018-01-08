from lark import Transformer
import sys

# TODO: this class is heavily coupled to Lark
# Is there a more abstract way to do this, so we can unit-test it better?
class HaxeTransformer(Transformer):

    def import_stmt(self, node):
        HaxeTransformer._LAST_NODE = node

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
