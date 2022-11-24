from dataclasses import dataclass
import sys
import ast
import argparse
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

def configureArgParser():
    argParser = argparse.ArgumentParser(description='List options')
    argParser.add_argument('-i', '--input', metavar='input', type=str, help='Path to input file', required=True)
    argParser.add_argument('-o', '--output', metavar='output', type=str, help='Path to output file', required=True)
    argParser.add_argument('-e', '--effective-vars', action='store', nargs='*', metavar='effective variables', type=str, help='List of effective variables to analyze; if omitted, target effective variables are found automatically.')
    argParser.add_argument('-v', '--verbose', action='store_true', help='Keep all unused functions if True')

    
    return argParser

if __name__ == "__main__":
    args = configureArgParser().parse_args()
    print(args)
    
    filepath = args.input 

    with open(filepath, 'r',encoding="utf8") as src_file:
        src = src_file.read()
        tree = ast.parse(src, mode='exec')

    state = AbstractState()
    programSlicerService = ProgramSlicerService()
    programSlicerService.slice(tree, state)
    print(f'Abstract state after program slicing:\n{str(state)}')
    print(f'effective vars = {programSlicerService.effectiveVars}')

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
