import ast
from typing import Type
from scalpel.cfg import Block

from model.abstractState import AbstractState
from utils.astUtils import ASTUtils

class ProgramSlicerService:

    def __init__(self, cfg):
        self.cfg = cfg
        self.astUtils = ASTUtils()
        '''The CFG to which we want to apply program slicing'''

    def slice(self, block: Block, state: AbstractState):

        statement: ast.AST
        for statement in block.statements:
                        
            if type(statement) is not ast.Assign:
                continue

            # TODO extract out into its own analyze or analyzeAssign function and write tests
            # we need to be careful that none of our future changes break existing behaviour
            # analyze(σ, n, x=e)

            # line number
            n = statement.lineno

            # targets can have length greater than one. For example, if we have a=b=1
            targets = statement.targets
            value = statement.value

            # S_l = L(0) ∪ L(1) ∪ ... ∪ L(|L|-1)
            S_l = set().union(*[list for list in state.L])

            for target in targets:
                
                if type(target) is ast.Name:
                
                    x = target.id
                    # S_e = M(y_0) ∪ M(y_1) ∪ ... ∪ M(y_n) where y_0,...,y_n are vars read in e
                    # TODO what if array of vars (Just THINK of more cases)
                    # TODO write tests for this, include array case
                    varsRead = self.astUtils.getAllVariables(value)
                    S_e = set().union(*[state.M.get(var, {}) for var in varsRead])
                    state.M[x] = set().union({n}, S_e, S_l)
                
                # Handle special cases like (a,b) = (1,2)
                elif type(target) is ast.Tuple and type(value) is ast.Tuple:

                    assert len(target.elts) == len(value.elts) # TODO raise exception and add appropriate error message

                    tNode: ast.Name
                    for i, tNode in enumerate(target.elts):

                        x = tNode.id
                        vNode = value.elts[i]
                        varsRead = self.astUtils.getAllVariables(vNode)
                        S_e = set().union(*[state.M.get(var, {}) for var in varsRead])
                        state.M[x] = set().union({n}, S_e, S_l)

                else:
                    print('UNEXPECTED')
                    # TODO raise exception, or is there another case we're not considering??

        return state

