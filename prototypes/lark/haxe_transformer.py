from lark import Transformer

class HaxeTransformer(Transformer):

    _LAST_NODE = None
    MARKER = "!!!"

    def import_stmt(self, node):
        HaxeTransformer._LAST_NODE = node

        output = "from "
        
        node = node[0].children # import_stmt => import_from
        package_name = node[0].children
        for child_node in package_name:
            output = "{}{}.".format(output, child_node.value)
        output = output[:-1] # trim last dot

        class_name = node[1].children[0].children[0].value
        output = "{} import {}".format(output, class_name)

        print("{} => {}".format(output, node))
        return output

    # def file_input(self, node):
    #     return HaxeTransformer.MARKER

    # def compound_stmt(self, node):
    #     return HaxeTransformer.MARKER

    # def funcdef(self, node):
    #     pass#return HaxeTransformer.MARKER

    # def funccall(self, node):
    #     return HaxeTransformer.MARKER