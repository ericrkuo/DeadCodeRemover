import ast
import pytest
from model.abstractState import AbstractState
from service.programSlicerService import ProgramSlicerService
from textwrap import dedent
import ast

class TestProgramSlicerService:

    def init(self, code):
        self.programSlicerService = ProgramSlicerService()
        tree = ast.parse(dedent(code).split('\n', 1)[1], mode='exec')
        self.state = AbstractState()
        self.programSlicerService.slice(tree, self.state)

    def assertState(self, expectedState: AbstractState):
        assert self.state.M == expectedState.M
        assert self.state.L == expectedState.L

    def assertEffectiveVars(self, expectedVars):
        assert self.programSlicerService.effectiveVars == expectedVars

    # -----------------#
    # ASSIGNMENT TESTS #
    # -----------------#

    def test_simpleAssignment(self):
        code = '''
        x = 42
        y = x
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {1,2}}

        self.assertState(expectedState)

    def test_assignmentDependsOnMultipleVariables(self):
        code = '''
        x = 42
        y = 10
        z = x + y
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {2}, 'z': {1,2,3}}

        self.assertState(expectedState)

    def test_assignmentDependsOnItself(self):
        code = '''
        x = 42
        y = 10
        z = x + y + z
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {2}, 'z': {1,2, 3}}

        self.assertState(expectedState)

    def test_assignValueToSameVariable(self):
        code = '''
        x = 42
        y = 10
        a = b = c = (x+y)
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {2}, 'a': {1,2,3}, 'b': {1,2,3}, 'c': {1,2,3}}

        self.assertState(expectedState)
    
    @pytest.mark.parametrize("input,output", [
        ("(a,b)", "(x+y,y)"),
        ("[a,b]", "(x+y,y)"),
        ("(a,b)", "[x+y,y]"),
        ("[a,b]", "[x+y,y]"),
    ])
    def test_assignTuplesOrLists(self, input, output):
        code = f'''
        x = 42
        y = 10
        {input} = {output}
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {2}, 'a': {1,2,3}, 'b': {2,3}}

        self.assertState(expectedState)

    @pytest.mark.parametrize("i1,i2,output", [
    ("(a,b)", "(c,d)", "(x+y,y)"),
    ("[a,b]", "(c,d)", "(x+y,y)"),
    ("(a,b)", "(c,d)", "[x+y,y]"),
    ("[a,b]", "(c,d)", "[x+y,y]"),
    ])
    def test_assignTuplesOrListsToSameVariables(self, i1, i2, output):
        code = f'''
        x = 42
        y = 10
        {i1} = {i2} = {output}
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {2}, 'a': {1,2,3}, 'b': {2,3}, 'c': {1,2,3}, 'd': {2,3},}

        self.assertState(expectedState)

    @pytest.mark.parametrize("value", [
    ("(x+y,y)"),
    ("(x+y,y)"),
    ("[x+y,y]"),
    ("[x+y,y]"),
    ])
    def test_assignIndicesOfArray(self, value):
        code = f'''
        x = 42
        y = 10
        a = [0]
        a[0] = {value}
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {2}, 'a': {1,2,4}}

        self.assertState(expectedState)

    def test_assignArrayDeclaration(self):
        code = '''
        x = 42
        y = 10
        a = 0
        a = [x + y, a]
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {2}, 'a': {1,2,3,4}}

        self.assertState(expectedState)

    def test_assignArray(self):
        code = '''
        x = 42
        y = 10
        z = x
        arr = [x,y,z]
        var1, var2, var3 = arr
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {2}, 'z': {1,3}, 'arr': {1,2,3,4},
            'var1': {1,2,3,4,5}, 'var2': {1,2,3,4,5}, 'var3': {1,2,3,4,5}}

        self.assertState(expectedState)

    def test_assignDictionary(self):
        code = '''
        x = 42
        y = 10
        dict = {x: 2, y: 4}
        var1, var2 = dict
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {2}, 'dict': {1,2,3},
            'var1': {1,2,3,4}, 'var2': {1,2,3,4}}

        self.assertState(expectedState)

    def test_assignSet(self):
        code = '''
        x = 42
        y = 10
        set = set([x,y])
        var1, var2 = set
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1,3}, 'y': {2,3}, 'set': {1,2,3},
            'var1': {1,2,3,4}, 'var2': {1,2,3,4}}

        self.assertState(expectedState)

    def test_assignFunctionCalls(self):
        code = '''
        a,b,c = 0,0,0
        y=0
        z=1
        x = foo(a,foo(b,c)) + [y,[z]]
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'a': {1,4}, 'b': {1,4}, 'c': {1,4}, 'y': {2}, 'z': {3}, 'x': {1,2,3,4}}

        self.assertState(expectedState)

    # ----------------------#
    # IF CONDITIONALS TESTS #
    # ----------------------#

    def test_basicif(self):
        code = '''
        x = 42
        y = 10
        b = 3
        if (x>y):
            a = b
        else:
            b = x    
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {2}, 'b': {1,2,3,7}, 'a': {1,2,3,5}}

        self.assertState(expectedState)

    def test_ifWithoutElse(self):
        code = '''
        x = 42
        y = 10
        b = 3
        if (x>y):
            a = b    
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {2}, 'b': {3}, 'a': {1,2,3,5}}

        self.assertState(expectedState)

    def test_nestedIfElse(self):
        code = '''
        x = 42
        y = 10
        b = 3
        if (x>y):
            a = b
            if (a>0):
                x = y + x
        else:
            b = x    
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1,2,7,3,5}, 'y': {2}, 'b': {1,2,3,9}, 'a': {1,2,3,5}}

        self.assertState(expectedState)

    def test_ifelifelse(self):
        code = '''
        x = 42
        y = 10
        b = 3
        if (x>y):
            a = b
        elif (x>0):
            y = b + b + y
        else:
            b = x    
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {2,7,1,3}, 'b': {1,2,3,9}, 'a': {1,2,3,5}}

        self.assertState(expectedState)

    def test_ifelifnoelse(self):
        code = '''
        x = 42
        y = 10
        b = 3
        if (x>y):
            a = b
        elif (x>0):
            y = b + b + y  
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {2,7,1,3}, 'b': {3}, 'a': {1,2,3,5}}

        self.assertState(expectedState)


    # ---------------------#
    # AUG ASSIGNMENT TESTS #
    # ---------------------#

    def test_simpleAugAssignment(self):
        code = '''
        x = 42
        y = 0
        y //= x
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {1,2,3}}

        self.assertState(expectedState)

    def test_arrayIndexAssignment(self):
        code = '''
        x = ['hello']
        y = ' world' 
        x[0] += y
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1,2,3}, 'y': {2}}

        self.assertState(expectedState) 
    
    # ---------------------#
    # LOOP STATEMENT TESTS #
    # ---------------------#
    
    def test_forLoopBasic(self):
        code = '''
        x = 42
        y = 2
        z = 1

        arr = [x, y, z]
        for val in arr:
            foo(val)
        '''  
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {2}, 'z': {3}, 'arr': {1,2,3,5}, 'val': {1,2,3,5,6,7}}

        self.assertState(expectedState)
    
    def test_forLoopWithRange(self):
        code = '''
        x = 42
        y = 2

        arr = [x, y]
        for i in range(len(arr)):
            if i == 0:
                x = y
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1,2,4,5,7}, 'y': {2}, 'i': {1,2,4,5}, 'arr': {1,2,4,5}}

        self.assertState(expectedState)

    
    def test_forLoopWithTuple(self):
        code = '''
        x = 42
        y = 2
        z = 1

        arr2 = [(x, y), (y, z), (x, z)]
        for i, j in arr2:
            print(i, j)
            x = x + 1
        ''' 
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1,2,3,5,6,8}, 'y': {2}, 'z':{3}, 'arr2': {1,2,3,5}, 'i': {1,2,3,5,6,7}, 'j': {1,2,3,5,6,7}}

        self.assertState(expectedState) 
    
    def test_whileLoopBasic(self):
        code = '''
        x = 1
        y = 2
        z = 1
        while z <= 5:
            y = y + x
        ''' 
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {1,2,3,5}, 'z':{3}}

        self.assertState(expectedState)
    
    def test_whileLoopWithArray(self):
        code = '''
        x = 1
        y = 2
        i = 0
        arr = [1, 2]
        while i <= 5:
          if i % 2 == 0:
            x = x + arr[i]
          else:
            y = y + arr[i]
        ''' 
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1,3,4,7}, 'y': {2,3,4,9}, 'i':{3}, 'arr': {4}}

        self.assertState(expectedState)

    # -----------#
    # FUNC TESTS #
    # -----------#

    def test_func_no_assign_with_side_effect(self):
        code = '''
        def fn(a):
            x = 2
            return a + x
        x = 3
        fn(x)
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {4, 5}, 'fn:x': {2}, }
        
        self.assertState(expectedState)

    def test_func_with_assign_should_differentiate_param_and_operand_vars(self):
        code = '''
        def fn(a):
            x = 2
            return a + x
        x = 3
        z = 5
        y = fn(x)+z
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {4, 6}, 'y': {4, 5, 6}, 'z': {5}, 'fn:x': {2}, }
        
        self.assertState(expectedState)

    def test_func_with_assign_should_differentiate_param_and_operand_vars(self):
        code = '''
        def fn(a):
            x = 2
            return a + x
        x = 3
        z = 5
        y = fn(x)+z
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {4, 6}, 'y': {4, 5, 6}, 'z': {5}, 'fn:x': {2}, }
        
        self.assertState(expectedState)

    def test_func_with_assign(self):
        code = '''
        def fn(a):
            x = 2
            return a + x
        x = 3
        y = fn(x)
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {4, 5}, 'y': {4, 5}, 'fn:x': {2}, }
        
        self.assertState(expectedState)

    def test_func_same_varname_should_not_conflict(self):
        code = '''
        x = 3
        def fn(a):
            x = 2
        y = fn(0)
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {4}, 'fn:x': {3}, }
        
        self.assertState(expectedState)

    def test_nested_func_calls_with_assign(self):
        code = '''
        x = 3
        def fn(a):
            x = 2
        def fn2(a):
            x = 2
        y = fn(fn2(0))
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {6}, 'fn:x': {3}, 'fn2:x': {5}}
        
        self.assertState(expectedState)

    def test_nested_func_calls_no_assign(self):
        code = '''
        x = 3
        def fn(a):
            x = 2
        def fn2(a):
            x = 2
        fn(fn2(0))
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'fn:x': {3}, 'fn2:x': {5}}
        
        self.assertState(expectedState)

    def test_nested_func_calls_no_assign_side_effect(self):
        code = '''
        x = 3
        def fn(a):
            x = 2
        def fn2(a):
            x = 2
        fn(fn2(x))
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {'x': {1, 6}, 'fn:x': {3}, 'fn2:x': {5}}
        
        self.assertState(expectedState)

    def test_effectiveVars_shouldPickReturnedVars(self):
        code = '''
        x = 2
        y = 5

        def fn(a, b):
            y = a
            a += 2
            z = y + a
            return z

        x = fn(1, 2)

        def fn2(a, b):
            z = 5

        fn2(1, fn2(1, 1))
        x = fn(fn2(1, 1), 1)
        '''
        self.init(code)

        expectedEffectiveVars = set({
            'fn:z'
        })

        self.assertEffectiveVars(expectedEffectiveVars)

    def test_effectiveVars_shouldPickArgs(self):
        code = '''
        x = 2
        y = 5

        def fn(a, b):
            y = a
            a += 2
            z = y + a
            return z

        x = fn(1, y)

        def fn2(a, b):
            z = 5

        fn2(1, fn2(1, 1))
        x = fn(fn2(1, 1), 1)
        '''
        self.init(code)

        expectedEffectiveVars = set({
            'fn:z',
            'y'
        })

        self.assertEffectiveVars(expectedEffectiveVars)

    def test_effectiveVars_shouldPickArgsWithinFunc(self):
        code = '''
        x = 2
        y = 5

        def fn(a, b):
            y = a
            a += 2
            z = y + a
            return z

        x = fn(1, 2)

        def fn2(a, b):
            z = 5
            print(a, b)

        fn2(1, fn2(1, 1))
        x = fn(fn2(1, 1), 1)
        '''
        self.init(code)

        expectedEffectiveVars = set({
            'fn:z',
            'fn2:a',
            'fn2:b'
        })

        self.assertEffectiveVars(expectedEffectiveVars)
