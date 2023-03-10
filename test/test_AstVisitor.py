import ast
from visitor.astVisitor import ASTVisitor


class TestASTVisitor:
    astVisitor = ASTVisitor()

    #---------------------------#
    # getAllReferencedVariables #
    #---------------------------#

    def test_simpleAssignment(self):
        code = 'x = y'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astVisitor.getAllReferencedVariables(tree)
        assert result == {'y'}

    def test_simpleAssignmentWithMoreThanOneVariable(self):
        code = 'x = x + y + 10 + z'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astVisitor.getAllReferencedVariables(tree)
        assert result == {'y', 'x', 'z'}

    def test_assignmentShouldIgnoreFunctionCallName(self):
        code = 'x = x + y + 10 + foo()'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astVisitor.getAllReferencedVariables(tree)
        assert result == {'y', 'x'}

    def test_assignmentShouldIgnoreFunctionCallAndKeepRelevantFunctionParameters(self):
        code = 'x = x + y + 10 + foo(a,b+c)'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astVisitor.getAllReferencedVariables(tree)
        assert result == {'y', 'x', 'a', 'b', 'c'}    

    def test_complexAssignmentFunctionCall(self):
        code = 'x = foo(a, b=c, *d, **e)'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astVisitor.getAllReferencedVariables(tree)
        assert result == {'a','c', 'd', 'e'}

    def test_complexAssignmentNestedFunctionCalls(self):
        code = 'x = foo(a, b=moo(c=hello))'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astVisitor.getAllReferencedVariables(tree)
        assert result == {'a','hello'}
        
    def test_arrayAssignment(self):
        code = 'x = [a, foo(b), d+e*2*y]'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astVisitor.getAllReferencedVariables(tree)
        assert result == {'a', 'b', 'd', 'e', 'y'}
        
    def test_setAssignment(self):
        code = 'x = set([a, foo(b), d+e*2*y])'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astVisitor.getAllReferencedVariables(tree)
        assert result == {'a', 'b', 'd', 'e', 'y'}
        
    def test_multiAssignment(self):
        code = 'a,b = {3: x, 5: y}'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astVisitor.getAllReferencedVariables(tree)
        assert result == {'x', 'y'}
        
    def test_evenMoreComplex(self):
        code = 'a = [int(myarray[i:i + 3], 2) for i in range(0, len(s), 3)]'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astVisitor.getAllReferencedVariables(tree)
        assert result == {'i', 's', 'myarray'}
    
    def test_ifStatement(self):
        code = 'x > 0'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astVisitor.getAllReferencedVariables(tree)
        assert result == {'x'}

    def test_ifStatementWithMultiVar(self):
        code = 'x == y + z'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astVisitor.getAllReferencedVariables(tree)
        assert result == {'x', 'y', 'z'}

    def test_shouldGetObjectWithAttributeCalls(self):
        code = 's = foo(queue.pop(0)) + stack.pop(0)'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astVisitor.getAllReferencedVariables(tree)
        assert result == {'queue', 'stack'}

    def test_shouldGetObjectWithAttributeCallsMoreComplex(self):
        code = 's = foo(queue.pop(a)) + stack.pop(queue2.pop(0))'
        tree = ast.parse(code)
        tree = tree.body[0].value # get ast.Assign.Value
        result = self.astVisitor.getAllReferencedVariables(tree)
        assert result == {'queue', 'stack', 'a', 'queue2'}

    #--------------------------------#
    # getUserDefinedFunctionCallVars #
    #--------------------------------#

    def test_getFunctionCallVariables(self):
        code = 'foo(a,b)'
        tree = ast.parse(code)
        tree = tree.body[0]
        result = self.astVisitor.getUserDefinedFunctionCallVars(tree, {'foo'})
        assert result == {'a', 'b'}

    def test_getFunctionCallVariablesShouldIgnoreIfNotUserDefinedFunction(self):
        code = 'range(a,b)'
        tree = ast.parse(code)
        tree = tree.body[0]
        result = self.astVisitor.getUserDefinedFunctionCallVars(tree, {})
        assert result == set()

    def test_getFunctionCallVariablesInAssignment(self):
        code = 'x = foo(a,b)'
        tree = ast.parse(code)
        tree = tree.body[0]
        result = self.astVisitor.getUserDefinedFunctionCallVars(tree, {'foo'})
        assert result == {'a', 'b'}

    def test_getFunctionCallVariablesMoreComplex(self):
        code = 'x = foo(a+c,b, [d,e], {f,g})'
        tree = ast.parse(code)
        tree = tree.body[0]
        result = self.astVisitor.getUserDefinedFunctionCallVars(tree, {'foo'})
        assert result == {'a', 'b', 'c', 'd', 'e', 'f', 'g'}

    def test_nestedFunctioncalls(self):
        code = 'x = foo(a, moo(b, boo(c+d)), self.hello([e]))'
        tree = ast.parse(code)
        tree = tree.body[0]
        result = self.astVisitor.getUserDefinedFunctionCallVars(tree, {'foo', 'moo', 'boo', 'hello'})
        assert result == {'a', 'b', 'c', 'd', 'e'}

    def test_nestedFunctioncallsShouldIgnoreVars(self):
        code = 'x = foo(a, moo(b, len(c+d)))'
        tree = ast.parse(code)
        tree = tree.body[0]
        result = self.astVisitor.getUserDefinedFunctionCallVars(tree, {'foo', 'moo'})
        assert result == {'a', 'b'}

    #------------------------------#
    # getAttributeFunctionCallVars #
    #------------------------------#

    def test_getAttributeObjects(self):
        code = 'x = a.foo(b)'
        tree = ast.parse(code)
        tree = tree.body[0]
        result = self.astVisitor.getAttributeFunctionCallVars(tree)
        assert result == {'a'}

    def test_shouldIgnorePropertyAccess(self):
        code = 'x = a.foo(b.foo)'
        tree = ast.parse(code)
        tree = tree.body[0]
        result = self.astVisitor.getAttributeFunctionCallVars(tree)
        assert result == {'a'}

    def test_shouldHandleNestedAttributeFunctionCalls(self):
        code = 'x = a.foo(b.foo(), c.moo(d.foo()))'
        tree = ast.parse(code)
        tree = tree.body[0]
        result = self.astVisitor.getAttributeFunctionCallVars(tree)
        assert result == {'a', 'b', 'c', 'd'}
