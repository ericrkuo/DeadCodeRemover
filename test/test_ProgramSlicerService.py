import ast
from model.abstractState import AbstractState
from service.programSlicerService import ProgramSlicerService
from scalpel.cfg import CFGBuilder
from textwrap import dedent

class TestProgramSlicerService:

    def init(self, code):
        self.cfg = CFGBuilder().build_from_src('cfg', dedent(code).split('\n', 1)[1])
        self.programSlicerService = ProgramSlicerService(self.cfg)
        # self.state = self.programSlicerService.sliceWith(self.cfg.entryblock, AbstractState())

        tree = ast.parse(dedent(code).split('\n', 1)[1], mode='exec')
        self.state = self.programSlicerService.sliceWithoutCFG(tree, AbstractState())

    def assertState(self, expectedState):
        assert self.state.M == expectedState.M
        assert self.state.L == expectedState.L

    def test_mytest(self):
        code = '''
        x = 42
        y = x
        '''
        self.init(code)

        expectedState = AbstractState()
        expectedState.M = {':x': {1}, ':y': {1,2}}
        
        self.assertState(expectedState)
    
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
        expectedState.M = {':x': {4, 5}, 'fn:x': {2}, }
        
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
        expectedState.M = {':x': {4, 5}, ':y': {4, 5}, 'fn:x': {2}, }
        
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
        expectedState.M = {':x': {1}, ':y': {4}, 'fn:x': {3}, }
        
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
        expectedState.M = {':x': {1}, ':y': {6}, 'fn:x': {3}, 'fn2:x': {5}}
        
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
        expectedState.M = {':x': {1}, 'fn:x': {3}, 'fn2:x': {5}}
        
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
        expectedState.M = {':x': {1, 6}, 'fn:x': {3}, 'fn2:x': {5}}
        
        self.assertState(expectedState)