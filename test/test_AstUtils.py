import ast
from src.utils.astUtils import ASTUtils


class TestASTUtils:
    astUtils = ASTUtils()

    def test_simpleAssignment(self):
        code = 'x = y'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astUtils.getAllVariables(tree)
        assert result == {'y'}

    def test_simpleAssignmentWithMoreThanOneVariable(self):
        code = 'x = x + y + 10 + z'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astUtils.getAllVariables(tree)
        assert result == {'y', 'x', 'z'}

    def test_simpleAssignmentShouldIgnoreFunctionCall(self):
        code = 'x = x + y + 10 + foo()'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astUtils.getAllVariables(tree)
        assert result == {'y', 'x', 'z'}
