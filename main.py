import sys
import ast
import argparse
from model.abstractState import AbstractState
from service.programSlicerService import ProgramSlicerService

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

