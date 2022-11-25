from dataclasses import dataclass
import os
import sys
import ast
import argparse
from typing import Dict
from model.abstractState import AbstractState
from service.programSlicerService import ProgramSlicerService
from ui.generateReport import ReportGenerator
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

    def __str__(self) -> str:
        return f'(Num_dependencies: {self.numDependencies}, variables: {self.variables}, source={self.source})'

def file_path(string):
    if os.path.isfile(string):
        return string
    else:
        raise argparse.ArgumentTypeError(f"'{string}' is not a valid path to a python file")

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise argparse.ArgumentTypeError(f"'{string}' is not a valid path to a directory")

def configureArgParser():
    argParser = argparse.ArgumentParser(description='List options')
    argParser.add_argument('-i', '--input', metavar='input', type=file_path, help='Path to input file', required=True)
    argParser.add_argument('-o', '--output', metavar='output', type=dir_path, help='Path to output directory', required=True)
    argParser.add_argument('-e', '--effective-vars', action='store', nargs='*', metavar='effective variables', type=str, help='Space-separated list of effective variables to analyze in the form of <function name>:<variable name> or <variable name>; if omitted, target effective variables are found automatically.')
    argParser.add_argument('-v', '--verbose', action='store_true', help='Keep all unused functions if True')
    argParser.add_argument('-d', '--debug', action='store_true', default=False, help='Debug mode prints out logs')
    
    return argParser

if __name__ == "__main__":
    args = configureArgParser().parse_args()
    
    filepath = args.input

    with open(filepath, 'r',encoding="utf8") as src_file:
        src = src_file.read()
        # we parse and unparse because python library doesn't handle newlines well
        src = ast.unparse(ast.parse(src, mode='exec'))
        tree = ast.parse(src, mode='exec')

    # Dependencies
    state = AbstractState()
    programSlicerService = ProgramSlicerService()
    lineNumberVisitor = LineNumberVisitor(src)
    programSliceTransformer = ProgramSliceTransformer()
    reportGenerator = ReportGenerator()

    # Slice the program and also find the effective vars
    programSlicerService.slice(tree, state)
    
    if args.effective_vars and len(args.effective_vars):
        effectiveVariables = args.effective_vars
    else:
        effectiveVariables = programSlicerService.effectiveVars
    
    effectiveLineNumbers = set().union(*[state.M.get(var, {}) for var in effectiveVariables])

    # Find the most dependented line numbers
    segment = lineNumberVisitor.getNodeWithLineNumber(tree)
    dependMap: Dict[int, DependentStat] = dict()
    for key, lineNums in state.M.items():
        for n in lineNums:
            stat = dependMap.get(n, DependentStat(0, set(), segment.get(n, "N/A")))
            stat.variables.add(key)
            stat.numDependencies += 1
            dependMap[n] = stat

    sortedTemp = sorted(dependMap.items(), key=lambda item: item[1].numDependencies)
    sortedTemp.reverse()
    dependMap = {k: v for k, v in sortedTemp}
    
    # Get the resulting program
    tree = programSliceTransformer.getSlicedProgram(effectiveLineNumbers, tree)

    # Get the removed line numbers
    removedLines = programSliceTransformer.removedLineNumbers.copy()

    # Get ratio of lines removed = # lines removed / total number of lines
    ratioLinesRemoved = len(removedLines) / len(src.split('\n'))

    # Generate map of effective variable to slice
    effectiveVariableMap = {}

    for effectiveVar in effectiveVariables:
        tempTree = ast.parse(src, mode='exec')
        tempLines = state.M.get(effectiveVar, set())
        tempTree = programSliceTransformer.getSlicedProgram(tempLines, tempTree)
        tempSrc = ast.unparse(tempTree)
        effectiveVariableMap[effectiveVar] = tempSrc

    reportGenerator.generateHTMLReport(
        outputDir=args.output,
        input = ast.unparse(ast.parse(src, mode='exec')), # ast.parse fixes some newlines/indentations
        output = ast.unparse(tree), 
        linesRemovedArr = removedLines,
        effectiveVariableMap = effectiveVariableMap,
        linesDependentOnMap=state.M,
        ratioLinesRemoved = ratioLinesRemoved,
        dependMap = dependMap,
        effectiveVariables = effectiveVariables,
        fileName = os.path.basename(args.input))

    # Debug mode
    if args.debug:
        print(f'Abstract state after program slicing:\n{str(state)}\n')
        print(f'effective vars = {effectiveVariables}\n')
        print(f'ORIGINAL CODE\n')
        print(src + '\n')
        print(effectiveLineNumbers)
        print("\n".join("  {}\t{}".format(k, v) for k, v in dependMap.items()))    
        print('removed line numbers: ', removedLines)
        print(f'SLICED PROGRAM for variable {effectiveVariables} \n')
        print(ast.unparse(tree) + '\n')
