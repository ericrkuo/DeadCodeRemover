import ast

class ASTVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functionCallsSeen = set()
        self.variablesSeen = set()
        
    def getAllFunctionCalls(self, node):
        '''
        Get's all variable names referneced in the given AST
        '''
        self.functionCallsSeen = set()
        super().visit(node)
        return self.functionCallsSeen

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
        for arg in node.args:
            self.visit(arg)

        for keyword in node.keywords:
            self.visit(keyword)
        
        # self.visit(node.func)
        self.functionCallsSeen.add(node.func.id)

    def visit_Name(self, node: ast.Name):
        self.variablesSeen.add(node.id)
