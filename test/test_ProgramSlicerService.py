from model.abstractState import AbstractState
from service.programSlicerService import ProgramSlicerService
from scalpel.cfg import CFGBuilder
from textwrap import dedent

class TestProgramSlicerService:

    def init(self, code):
        self.state = AbstractState()
        self.cfg = CFGBuilder().build_from_src('cfg', dedent(code).split('\n', 1)[1])
        self.programSlicerService = ProgramSlicerService(self.cfg)

    def test_mytest(self):
        code = '''
        x = 42
        y = x
        '''
        self.init(code)
        self.state = self.programSlicerService.slice(self.cfg.entryblock, self.state)

        expectedState = AbstractState()
        expectedState.M = {':x': {1}, ':y': {1,2}}
        
        assert self.state.M == expectedState.M
        assert self.state.L == expectedState.L
    