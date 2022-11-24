import sys
import ast
from model.abstractState import AbstractState
from service.programSlicerService import ProgramSlicerService
from visitor.lineNumberVisitor import LineNumberVisitor
from visitor.programSliceTransformer import ProgramSliceTransformer

if __name__ == "__main__":
    args = sys.argv[1:]
    assert len(args) == 1
    filepath = args[0]

    with open(filepath, 'r',encoding="utf8") as src_file:
        src = src_file.read()
        tree = ast.parse(src, mode='exec')

    state = AbstractState()
    programSlicerService = ProgramSlicerService(src)
    programSlicerService.slice(tree, state)
    print(f'Abstract state after program slicing:\n{str(state)}\n')

    # TODO integrate with earlier pipelines - getting effective vars and resulting lines to keep from merged slices
    print(f'ORIGINAL CODE\n')
    print(src + '\n')
    effectiveVariables = list(state.M.keys())[:4]
    
    effectiveLineNumbers = set().union(*[state.M[var] for var in effectiveVariables])
    print(effectiveLineNumbers)
    # find most dependented line numbers
    lineNumberVisitor = LineNumberVisitor(src)
    segment = lineNumberVisitor.getNodeWithLineNumber(tree)
    # print('segment:', segment)
    dependMap = dict()
    for key, lineNums in state.M.items():
        for ln in lineNums:
            currDepend, varSet, srcSeg = dependMap.get(ln, (0, set(), segment[ln]))
            varSet.add(key)
            dependMap[ln] = (currDepend + 1, varSet, srcSeg)
    # print(dependMap)
    dependList = sorted([(key, value[0], value[1], value[2]) for key, value in dependMap.items()], key=lambda x: x[1])
    print(dependList)
    
    programSliceTransformer = ProgramSliceTransformer()
    tree = programSliceTransformer.getSlicedProgram(effectiveLineNumbers, tree)
    print('removed line numbers: ', programSliceTransformer.removedLineNumbers)
    print(f'SLICED PROGRAM for variable {effectiveVariables} \n')
    print(ast.unparse(tree) + '\n')
