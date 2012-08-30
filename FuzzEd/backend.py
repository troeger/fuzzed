import ast, minbool

class MinBool(ast.NodeVisitor):
    def __init__(self):
        self.current=[]
        self.result=[]

    def simplify(self, boolterm):
        res = minbool.simplify(boolterm)
        self.visit(res.ast())
        return self.result

    def generic_visit(self, arg):
        super(MinBool, self).generic_visit(arg)
        if self.current != []:
            self.result.append(self.current)
        self.current=[]

    def visit_Name(self, name):
        self.current.append(str(name.id))

    def visit_Or(self, boolop):
        self.generic_visit(boolop)

    def visit_And(self, boolop):
        self.generic_visit(boolop)
