import ast

class ASTUtils:

    def getAllReferencedVariables(self, tree: ast.AST):
        '''Gets all variables referenced inside the provided ast node'''
        # TODO this is failing test case - need to exclude function calls
        # https://stackoverflow.com/a/33554224 
        return {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}