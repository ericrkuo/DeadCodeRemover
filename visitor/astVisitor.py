import ast

class ASTVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functionCallsSeen = set()
        self.functionCallArgs = set()
        self.variablesSeen = set()
        self.context = []
        
    def getAllFunctionCallVars(self, node):
        '''
        Get all variable names referenced in a function call
        '''
        self.functionCallArgs = set()
        super().visit(node)
        return self.functionCallArgs

    def getAllReferencedVariables(self, node):
        '''
        Get's all variable names referneced in the given AST

        Inspiration: https://stackoverflow.com/a/43166653
        '''
        self.variablesSeen = set()
        super().visit(node)
        return self.variablesSeen

    def visit_Call(self, node: ast.Call):
        '''Only visit the args and keywords of a Call statement'''
        self.context.append('call')
        for arg in node.args:
            self.visit(arg)

        for keyword in node.keywords:
            self.visit(keyword)
        
        # self.visit(node.func)
        self.functionCallsSeen.add(node.func.id)
        self.context.pop()

    def visit_Name(self, node: ast.Name):
        self.variablesSeen.add(node.id)

        if (len(self.context) and self.context[-1] == 'call'):
            self.functionCallArgs.add(node.id)
