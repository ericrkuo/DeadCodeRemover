from dataclasses import dataclass
import sys
import ast
from typing import Dict
from model.abstractState import AbstractState
from service.programSlicerService import ProgramSlicerService
from visitor.lineNumberVisitor import LineNumberVisitor
from visitor.programSliceTransformer import ProgramSliceTransformer


@dataclass
class DependentStat:
    '''
    Represent a dependency statistic
    - `numDependencies` represents how many variables are dependent on the current line
    - `variables` shows the variables
    - `source` represents the source code at that line number
    '''
    numDependencies: int
    variables: set
    source: str

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

    # TODO integrate with earlier pipelines - getting effective vars
    # TODO integrate with later pipelines - Jin UI
    print(f'ORIGINAL CODE\n')
    print(src + '\n')
    effectiveVariables = list(state.M.keys())[:4]
    
    effectiveLineNumbers = set().union(*[state.M[var] for var in effectiveVariables])
    print(effectiveLineNumbers)
    # find most dependented line numbers
    lineNumberVisitor = LineNumberVisitor(src)
    segment = lineNumberVisitor.getNodeWithLineNumber(tree)
    dependMap: Dict[int, DependentStat] = dict()
    for key, lineNums in state.M.items():
        for n in lineNums:
            # TODO remove "N/A" once we fix mapping of line number to source code
            stat = dependMap.get(n, DependentStat(0, set(), segment.get(n, "N/A")))
            stat.variables.add(key)
            stat.numDependencies += 1
            dependMap[n] = stat

    dependMap = {k: v for k, v in sorted(dependMap.items(), key=lambda item: item[1].numDependencies)}
    print("\n".join("  {}\t{}".format(k, v) for k, v in dependMap.items()))
    
    programSliceTransformer = ProgramSliceTransformer()
    tree = programSliceTransformer.getSlicedProgram(effectiveLineNumbers, tree)
    print('removed line numbers: ', programSliceTransformer.removedLineNumbers)
    print(f'SLICED PROGRAM for variable {effectiveVariables} \n')
    print(ast.unparse(tree) + '\n')
