import ast
from src.utils.astUtils import ASTUtils


class TestASTUtils:
    astUtils = ASTUtils()

    def test_simpleAssignment(self):
        code = 'x = y'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astUtils.getAllReferencedVariables(tree)
        assert result == {'y'}

    def test_simpleAssignmentWithMoreThanOneVariable(self):
        code = 'x = x + y + 10 + z'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astUtils.getAllReferencedVariables(tree)
        assert result == {'y', 'x', 'z'}

    def test_simpleAssignmentShouldIgnoreFunctionCall(self):
        code = 'x = x + y + 10 + foo()'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astUtils.getAllReferencedVariables(tree)
        assert result == {'y', 'x'}

    def test_simpleAssignmentShouldIgnoreFunctionCallAndKeepRelevantFunctionParameters(self):
        code = 'x = x + y + 10 + foo(a,b+c)'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astUtils.getAllReferencedVariables(tree)
        assert result == {'y', 'x', 'a', 'b', 'c'}
