import ast
from typing import Type
from scalpel.cfg import Block

from model.abstractState import AbstractState
from visitor.astVisitor import ASTVisitor

class ProgramSlicerService:

    def __init__(self, cfg):
        self.cfg = cfg
        self.astVisitor = ASTVisitor()
        '''The CFG to which we want to apply program slicing'''

    def slice(self, block: Block, state: AbstractState):

        statement: ast.AST
        for statement in block.statements:

            if type(statement) is not ast.Assign:
                continue
            
            self.analyzeAssign(state, statement)

        # TODO handle loops, conditionals, etc.

        return state

    # TODO write tests, we need to be careful that none of our future changes break existing behaviour
    def analyzeAssign(self, state: AbstractState, statement: ast.Assign):
        '''
        Run the program slicing analysis function analyze(σ, n, ast.Assign).

        We build upon the analysis function learned from lecture since Python can have multiple assignments in a single line.

        ## Algorithm:
        ```
        Let X be the set of variables assigned {x_1, x_2, ..., x_n}
        Let E_i be the set of variables read for variable x_i

        For each x_i in X
            M[x_i -> {n} ∪ S_e ∪ S_l]
            where S_e = M(y_0) ∪ ... ∪ M(y_n) where y_0:n are the variables read in E_i
                  S_l = L(0) ∪ ... ∪ L(|L|-1) which is the union of all sets stored in the list
        ```
        '''
         # line number
        n = statement.lineno

        # An assignment call have have more than one target. For example, if we have a=b=1, the two targets are a and b
        # See https://docs.python.org/3/library/ast.html#ast.Assign for more details
        targets = statement.targets
        value = statement.value

        for target in targets:
            
            if type(target) is ast.Name:
                self.updateState(state, target.id, value, n)
            
            # Handle special cases like (a,b) = (1,2)
            elif type(target) is ast.Tuple and type(value) is ast.Tuple:
                if (len(target.elts) != len(value.elts)):
                    raise Exception('Unexpected error: the number of target variables does not equal the number of values assigned')

                tNode: ast.Name
                for i, tNode in enumerate(target.elts):
                    vNode = value.elts[i]
                    self.updateState(state, tNode.id, vNode, n)

            # Handle unpacking cases like a,b,c = arr where arr = [1,2,3]
            elif type(target) is ast.Tuple and type(value) is ast.Name:
                tNode: ast.Name
                for i, tNode in enumerate(target.elts):
                    self.updateState(state, tNode.id, value, n)
   
            else:
                raise Exception(f'Unexpected error: encountered unsupported target in an assignment call {target}')

    def updateState(self, state: AbstractState, targetVariable, value: ast.AST, n):
        '''
        Args:
            state: the abstract state pair (M,L) to update.
            targetVariable: the name of the target variable
            value: the ast node being assigned to the target variable
            n: the line number of the statement
        '''
        varsRead = self.astVisitor.getAllReferencedVariables(value)
        S_l = set().union(*[list for list in state.L])
        S_e = set().union(*[state.M.get(var, {}) for var in varsRead])
        state.M[targetVariable] = set().union({n}, S_e, S_l)
