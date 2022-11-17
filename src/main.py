import sys
import ast
from scalpel.cfg import CFGBuilder
from model.abstractState import AbstractState
from service.programSlicerService import ProgramSlicerService

if __name__ == "__main__":
    args = sys.argv[1:]
    
    assert len(args) == 1

    filepath = args[0]
    cfg = CFGBuilder().build_from_file('cfg', filepath)

    state = AbstractState()
    programSlicerService = ProgramSlicerService(cfg)
    
    state = programSlicerService.slice(cfg.entryblock, state)
    print(f'Abstract state after program slicing:\n{str(state)}')