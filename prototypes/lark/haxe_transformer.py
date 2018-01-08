from lark import Transformer

class HaxeTransformer(Transformer):

    _LAST_NODE = None

    def import_from(self, node):
        HaxeTransformer._LAST_NODE = node

        output = "from "
        
        package_name = node[0].children
        for child_node in package_name:
            output = "{}{}.".format(output, child_node.value)
        output = output[:-1] # trim last dot

        class_name = node[1].children[0].children[0].value
        output = "{} import {}".format(output, class_name)

        print("{} => {}".format(output, node))
        return output
