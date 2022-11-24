import ast
from typing import Any


class LineNumberVisitor(ast.NodeVisitor):
  
    def __init__(self, src: str) -> None:
        super().__init__()
        self.segmentMap = dict()
        self.source = src
    
    def getNodeWithLineNumber(self, node: ast.AST):
        super().visit(node)
        return self.segmentMap
  
    def generic_visit(self, node: ast.AST) -> Any:
        # get the source string per line
        srcSegment = ast.get_source_segment(self.source, node)
        if srcSegment:
            # print(node.lineno, srcSegment)
            self.segmentMap[node.lineno] = srcSegment
        
        super().generic_visit(node)
        return self.segmentMap

    def visit_For(self, node: ast.For):
        super().visit_For(node)
        return self.segmentMap

    def visit_If(self, node: ast.If):
        super().visit_If(node)
        return self.segmentMap
    
    def visit_While(self, node: ast.While) -> Any:
        super().visit_While(node)
        return self.segmentMap
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        super().visit_FunctionDef(node)
        return self.segmentMap
  