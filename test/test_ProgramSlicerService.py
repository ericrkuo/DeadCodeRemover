from model.abstractState import AbstractState
from service.programSlicerService import ProgramSlicerService
from scalpel.cfg import CFGBuilder
from textwrap import dedent
import ast

class TestProgramSlicerService:

    def test_mytest(self):
        code = '''
        x = 42
        y = x
        '''

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {1,2}}

        cfg = CFGBuilder().build_from_src('cfg', dedent(code).split('\n', 1)[1])
        state = AbstractState()
        programSlicerService = ProgramSlicerService(cfg)
        state = programSlicerService.slice(cfg.entryblock, state)
        # state = programSlicerService.sliceWithoutCFG(ast.parse(code, mode='exe'), state)
        
        assert state.M == expectedState.M
        assert state.L == expectedState.L
