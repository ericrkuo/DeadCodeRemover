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
    variable = list(state.M.keys())[0]
    programSliceTransformer = ProgramSliceTransformer()
    tree = programSliceTransformer.getSlicedProgram(state.M[variable], tree)
    print(f'SLICED PROGRAM for variable {variable} \n')
    print(ast.unparse(tree) + '\n')
