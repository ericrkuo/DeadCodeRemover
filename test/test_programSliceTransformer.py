import ast
from textwrap import dedent
from service.programSlicerService import ProgramSlicerService
from visitor.programSliceTransformer import ProgramSliceTransformer


class TestProgramSliceTransformer:
    programSliceTransformer = ProgramSliceTransformer()

    def sliceProgramAndAssert(self, code, lineNumbers, expectedCode):
        tree = ast.parse(dedent(code).split('\n', 1)[1], mode='exec')
        result = self.programSliceTransformer.getSlicedProgram(lineNumbers, tree)
        assert ast.unparse(result) == dedent(expectedCode).strip()

    def test_getSlicedProgramNoControlFlow(self):
        code = '''
        x = 42
        y = 10
        a = 0
        z = x + y
        b += a
        '''

        expectedCode = '''
        x = 42
        y = 10
        z = x + y
        '''
        self.sliceProgramAndAssert(code, {1,2,4}, expectedCode)

    def test_entireIfShouldBeRemovedIfBothBlocksEmpty(self):
        code = '''
        x = 42
        a = 0
        if x:
            y = 1
        else:
            y += 1
        '''

        expectedCode = '''
        a = 0
        '''
        self.sliceProgramAndAssert(code, {2}, expectedCode)    

    def test_emptyThenBlockShouldBeReplacedWithPass(self):
        code = '''
        x = 42
        a = 0
        if x:
            y = 1
        else:
            a += 1
        '''

        expectedCode = '''
        x = 42
        a = 0
        if x:
            pass
        else:
            a += 1
        '''
        self.sliceProgramAndAssert(code, {1,2,6}, expectedCode)    

    def test_emptyElseBlockShouldBeDeleted(self):
        code = '''
        x = 42
        a = 0
        if x:
            a += 1
        else:
            y = 1
        '''

        expectedCode = '''
        x = 42
        a = 0
        if x:
            a += 1
        '''
        self.sliceProgramAndAssert(code, {1,2,4}, expectedCode)    

    def test_emptyElifShouldBeReplacedWithPass(self):
        code = '''
        x = 42
        a = 0
        if x:
            a += 1
        elif a:
            a = x + a
        else:
            y = 1
        '''

        expectedCode = '''
        x = 42
        a = 0
        if x:
            a += 1
        elif a:
            pass
        else:
            y = 1
        '''
        self.sliceProgramAndAssert(code, {1,2,4,8}, expectedCode)    

    def test_emptyElseShouldJustKeepElif(self):
        code = '''
        x = 42
        a = 0
        if x:
            a += 1
        elif a:
            a = x + a
        else:
            y = 1
        '''

        expectedCode = '''
        x = 42
        a = 0
        if x:
            a += 1
        elif a:
            a = x + a
        '''
        self.sliceProgramAndAssert(code, {1,2,4,6}, expectedCode)    

    def test_nestedIfsShouldBeHandledAccordingly(self):
        code = '''
        x = 42
        a = 0
        if x:
            a += 1
            if a:
                b = 0
            else:
                b //= a
        elif a:
            a = x + a
            if a:
                b = 0
            else:
                b //= a
        else:
            y = 1
            if a:
                b = 0
            else:
                b //= a
        '''

        expectedCode = '''
        x = 42
        a = 0
        if x:
            a += 1
            if a:
                pass
            else:
                b //= a
        elif a:
            if a:
                b = 0
        else:
            y = 1
        '''
        self.sliceProgramAndAssert(code, {1,2,4,8,12,16}, expectedCode)    

    def test_shouldNotRemoveTheFollowingItems(self):
        '''
        Do not remove
        1. Function calls
        2. Function declarations
        3. Return statements
        4. Imports
        '''

        code = '''
        import os

        def foo(a, b):
            x = 0
            y += x
            print(y)
            print(range(len(x)))
            return (a + b, [x])

        x = [1, 2, 3]
        print(y)
        foo(0, x)
        '''

        expectedCode = '''
        import os

        def foo(a, b):
            x = 0
            print(y)
            print(range(len(x)))
            return (a + b, [x])
        x = [1, 2, 3]
        print(y)
        foo(0, x)
        '''

        self.sliceProgramAndAssert(code, {4,10}, expectedCode)

    def test_shouldKeepItemsInWhileLoop(self):
        code = '''
        while x:
            print(a)
            b += foo(a,b)
        '''

        expectedCode = '''
        while x:
            print(a)
        '''

        self.sliceProgramAndAssert(code, {2}, expectedCode)

    def test_shouldKeepItemsInForLoop(self):
        code = '''
        for x in range(n):
            print(a)
            b += foo(a,b)
        '''

        expectedCode = '''
        for x in range(n):
            print(a)
        '''

        self.sliceProgramAndAssert(code, {2}, expectedCode)

    def test_shouldDeleteEntireWhileLoopIfNoStatementsKeptInside(self):
        code = '''
        y = 0
        while x:
            c *= 1
            b += foo(a,b)
        foo([a, b])
        '''

        expectedCode = '''
        y = 0
        foo([a, b])
        '''

        self.sliceProgramAndAssert(code, {1,5}, expectedCode)

    def test_shouldDeleteEntireForLoopIfNoStatementsKeptInside(self):
        code = '''
        y = 0
        for x in range(n):
            c *= 1
            b += foo(a,b)
        foo([a, b])
        '''

        expectedCode = '''
        y = 0
        foo([a, b])
        '''

        self.sliceProgramAndAssert(code, {1,5}, expectedCode)

    def test_shouldKeepForLoopEvenIfOnlyFunctionCallInside(self):
        code = '''
        y = 0
        for x in range(n):
            c *= 1
            moo(a)
            b += boo(a,b)
        foo([a, b])
        '''

        expectedCode = '''
        y = 0
        for x in range(n):
            moo(a)
        foo([a, b])
        '''

        self.sliceProgramAndAssert(code, {1,6}, expectedCode)
