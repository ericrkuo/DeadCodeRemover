import sys
import ast
from model.abstractState import AbstractState
from service.programSlicerService import ProgramSlicerService

if __name__ == "__main__":
    args = sys.argv[1:]
    assert len(args) == 1
    filepath = args[0]

    with open(filepath, 'r',encoding="utf8") as src_file:
        src = src_file.read()
        tree = ast.parse(src, mode='exec')

    state = AbstractState()
    programSlicerService = ProgramSlicerService()
    programSlicerService.slice(tree, state)
    print(f'Abstract state after program slicing:\n{str(state)}')
