import ast, minbool

class MinBool(ast.NodeVisitor):
    def __init__(self):
        self.current=[]
        self.result=[]
        self.inOr=False

    def simplify(self, boolterm):
        res = minbool.simplify(boolterm)
        self.visit(res.ast())
        return self.result

    def generic_visit(self, arg):
        #print "Arg: "+str(arg)
        super(MinBool, self).generic_visit(arg)
        #print "Current: "+str(self.current)
        if self.current != []:
            self.result.append({'nodes':self.current})
            self.current=[]

    def visit_Name(self, name):
        self.current.append(str(name.id))

    def visit_Num(self, num):
        #print "Num: "+str(num)
        if self.inOr:
            #print "inor"
            self.result.append({'nodes':[num.n]})
        else:
            #print "inand"
            self.current.append(num.n)

    def visit_Or(self, boolop):
        #print "OR"
        self.inOr=True
        self.generic_visit(boolop)

    def visit_And(self, boolop):
        #print "AND"
        self.inOr=False
        self.generic_visit(boolop)
