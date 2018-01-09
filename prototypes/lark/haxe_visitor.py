from lark.tree import Visitor

class HaxeVisitor(Visitor):
    
    LAST_NODE = None

    def process(self, tree):
        return self.visit(tree)
    
    def import_from(self, node):
        print("@@@@@ NODE {}".format(node))
        output = "import "
        HaxeVisitor.LAST_NODE = node

        #node = node.children[0].children[0] # import_stmt => import_from
        # package_name = node.children[0].children[0].value

        # x = """
        # >>> node.children[0].children[0].value
        # 'flixel'
        # >>> node.children[1].children[0].children[0].value
        # 'FlxGame'
        # """

        package_tree = node.children[0].children
        class_name = node.children[1].children[0].children[0].value

        for package_node in package_tree:
            output = "{}{}.".format(output, package_node.value)

        output = "{}{}".format(output, class_name)

        print("i={} o={}".format(node, output))
        return output
