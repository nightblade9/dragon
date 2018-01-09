from lark.tree import Visitor

class HaxeVisitor(Visitor):
    def process(self, tree):
        return self.visit(tree)
    
    def import_stmt(self, data):
        print("IMPORT {}".format(data))
    
    def compound_stmt(self, data):
        print("COMP".format(data))