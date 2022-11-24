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
        if srcSegment and node.lineno not in self.segmentMap:
            srcSegment = srcSegment.split('\n')[0]
            # print(node.lineno, srcSegment)
            self.segmentMap[node.lineno] = srcSegment
        
        super().generic_visit(node)
        return self.segmentMap
  