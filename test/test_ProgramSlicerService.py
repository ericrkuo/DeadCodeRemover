from model.abstractState import AbstractState
from service.programSlicerService import ProgramSlicerService
from scalpel.cfg import CFGBuilder

class TestProgramSlicerService:

    def test_mytest(self):
        code = '''
        x = 42
        y = x
        '''

        expectedState = AbstractState()
        expectedState.M = {'x': {1}, 'y': {1,2}}

        cfg = CFGBuilder().build_from_src('cfg', code)
        state = AbstractState()
        programSlicerService = ProgramSlicerService(cfg)
        state = programSlicerService.slice(cfg.entryblock, state)
        
        assert state == expectedState
