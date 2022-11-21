import ast
from service.programSlicerService import ProgramSlicerService
from model.abstractState import AbstractState

class ProgramSlicerService:
  
    def __init__(self, tree: ast.Module):
        self.state = AbstractState()
        programSlicerService = ProgramSlicerService()
        programSlicerService.slice(tree, self.state)
    
    def getFinalState(self):
        return self.state

    def getSlicedProgramWithVariable(self, vars: set):
        setOfLineNums = set().union(*[self.state.M.get(var, {}) for var in vars])
        return setOfLineNums
