import sys
import ast
from model.abstractState import AbstractState
from service.programSlicerService import ProgramSlicerService
from visitor.programSliceTransformer import ProgramSliceTransformer

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
    print(f'Abstract state after program slicing:\n{str(state)}\n')

    # TODO integrate with earlier pipelines - getting effective vars and resulting lines to keep from merged slices
    print(f'ORIGINAL CODE\n')
    print(src + '\n')
    effectiveVariables = list(state.M.keys())[:4]
    
    effectiveLineNumbers = set().union(*[state.M[var] for var in effectiveVariables])
    print(effectiveLineNumbers)
    # find most dependented line numbers
    dependMap = dict()
    for key, lineNums in state.M.items():
        for ln in lineNums:
            dependMap[ln] = dependMap.get(ln, 0) + 1
    dependList = sorted(list(dependMap.items()), key=lambda x: x[1])
    # print(dependList)
    
    programSliceTransformer = ProgramSliceTransformer()
    tree = programSliceTransformer.getSlicedProgram(effectiveVariables, tree)
    print(f'SLICED PROGRAM for variable {effectiveVariables} \n')
    print(ast.unparse(tree) + '\n')
