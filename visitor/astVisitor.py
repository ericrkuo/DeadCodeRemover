import ast

class ASTVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functionCallVars = set()
        self.variablesSeen = set()
        self.attributeCallVars = set()
        self.functionDefNames = set()
        self.context = []
 
    def getUserDefinedFunctionCallVars(self, node, functionDefNames):
        '''
        Get the name of all variables referenced in user defined function calls
        '''
        self.functionDefNames = functionDefNames
        self.functionCallVars = set()
        super().visit(node)
        return self.functionCallVars.copy()

    def getAllReferencedVariables(self, node):
        '''
        Get's all variable names referneced in the given AST

        Inspiration: https://stackoverflow.com/a/43166653
        '''
        self.variablesSeen = set()
        super().visit(node)
        return self.variablesSeen.copy()

    def getAttributeFunctionCallVars(self, node):
        '''
        Get the name of all attribute function calls. E.g. we want obj in obj.func(...)
        '''
        self.attributeCallVars = set()
        super().visit(node)
        return self.attributeCallVars.copy()

    def visit_Call(self, node: ast.Call):
        '''Only visit the args and keywords of a Call statement'''

        if type(node.func) is ast.Name:
            self.context.append(node.func.id)
        elif type(node.func) is ast.Attribute and type(node.func.value) is ast.Name:
            self.attributeCallVars.add(node.func.value.id)
            # add to variablesSeen because we should still count object b as a variable seen if we have a = b.foo()
            self.variablesSeen.add(node.func.value.id)

        for arg in node.args:
            self.visit(arg)

        for keyword in node.keywords:
            self.visit(keyword)
        
        if type(node.func) is ast.Name:
            self.context.pop()

    def visit_Name(self, node: ast.Name):
        self.variablesSeen.add(node.id)

        if (len(self.context) and self.functionDefNames and self.context[-1] in self.functionDefNames):
            self.functionCallVars.add(node.id)
