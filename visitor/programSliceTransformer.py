import ast
from model.abstractState import AbstractState

class ProgramSliceTransformer(ast.NodeTransformer):

    def getSlicedProgram(self, lineNumbers: set, node: ast.AST) -> ast.AST:
        '''
        Returns the AST with only the lines in `node` specified by `lineNumbers`.

        However, certain control flow statements like ifs, for loops, while loops are handled differently.

        Furthermore, imports, return statements, function calls, function declarations will all be kept.
        '''

        self.lineNumbers = lineNumbers

        return self.generic_visit(node)
    
    def visit_Assign(self, node: ast.Assign):
        if (node.lineno not in self.lineNumbers):
            return None
        
        return node
    
    def visit_AugAssign(self, node: ast.AugAssign):
        if (node.lineno not in self.lineNumbers):
            return None
        
        return node

    def visit_If(self, node: ast.If):
        result: ast.If = self.generic_visit(node)

        body = result.body
        orElse = result.orelse

        if len(body) == 0 and len(orElse) == 0:
            return None
        
        # empty body should just be replaced with pass, the orelse block may have important information to keep
        if len(body) == 0:
            body.append(ast.Pass())

        return result

    def visit_For(self, node: ast.For):
        result: ast.For = self.generic_visit(node)

        if len(result.body) == 0:
            return None

        return result

    def visit_While(self, node: ast.While):
        result: ast.For = self.generic_visit(node)

        if len(result.body) == 0:
            return None

        return result
        