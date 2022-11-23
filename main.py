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
    print(f'effective vars = {programSlicerService.effectiveVars}')
    print(f'func calls lines = {programSlicerService.funcCalls}')


    # Policy of choosing effective variables and lines to keep
    # 1. keep all func call
    # 2. keep all effective vars and lines they depend on
    # 3. variables passed to functions are effective
    # (4. all func args are effective within function scope)
    # 5. if a func tries to reference a variable that's not in the map of the states, that variable is a out-of-scope var,
    # which should be effective

    # TODO include retunred line in dependency list
