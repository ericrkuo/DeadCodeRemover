import ast

class FunctionDeclarationVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functionNames: set = set()
        
    def getAllFunctionDefinitionNames(self, node):
        '''
        Get all function definition names
        '''
        self.functionNames = set()
        super().visit(node)
        return self.functionNames

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.functionNames.add(node.name)

        # visit all children of the node - handles nested function definitions
        self.generic_visit(node)
