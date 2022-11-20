import ast

from model.abstractState import AbstractState
from visitor.astVisitor import ASTVisitor

class ProgramSlicerService:

    def __init__(self):
        self.astVisitor = ASTVisitor()

    def slice(self, node: ast.AST, state: AbstractState):
        '''Run program slicing starting from the given `node`. Modify `state` in place, which is why the method has no return value'''
        if type(node) is ast.Module:
            for child in node.body:
                self.slice(child, state)

        elif type(node) is ast.Assign:
              self.analyzeAssign(state, node)

        elif type(node) is ast.If:
            self.analyzeIf(state, node)
        
    def analyzeIf(self, state: AbstractState, statement: ast.If):
        '''
        Handle program slicing for an if statement.

        Algorithm:

        1. Update the L stack with the mapping of the current varibales in the condition
        2. Run program slicing across the then block `ast.If::body`
        3. Run program slicing across the else block `ast.If::orelse` (if one exists)
        4. We then union the resulting states from 1 and 2
        5. Pop the L stack
        '''
        varsInCondition = self.astVisitor.getAllReferencedVariables(statement.test)

        curr_L = set().union(*[state.M.get(var, {}) for var in varsInCondition])
        state.L.append(curr_L)

        bodyState = state.copy()
        orElseState = state.copy()
        
        for node in statement.body:
            self.slice(node, bodyState)
        
        for node in statement.orelse:
            self.slice(node, orElseState)

        # Union the resulting states
        unionVars = set().union(bodyState.M.keys(), orElseState.M.keys())
        state.M = dict()
        for var in unionVars:
            state.M[var] = set().union(bodyState.M.get(var, {}), orElseState.M.get(var, {}))
        state.L.pop()

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
            
            elif (type(target) is ast.Tuple or type(target) is ast.List):

                # Handle cases like (a,b) = (1,2) | [a,b] = (1,2) | (a,b) = [1,2] | [a,b] = [1,2]    
                if type(value) is ast.Tuple or type(value) is ast.List:
                    if (len(target.elts) != len(value.elts)):
                        raise Exception('Unexpected error: the number of target variables does not equal the number of values assigned')

                    tNode: ast.Name
                    for i, tNode in enumerate(target.elts):
                        vNode = value.elts[i]
                        self.updateState(state, tNode.id, vNode, n)

                # Handle unpacking cases like a,b,c = arr | [a,b,c] = arr where arr = [1,2,3]
                elif type(value) is ast.Name:
                    tNode: ast.Name
                    for i, tNode in enumerate(target.elts):
                        self.updateState(state, tNode.id, value, n)

            # Handle cases like a[2] = b | a[2] = (1,2) | a[2] = [1,2] | a[1:2] = [1,2]
            # Note: we don't care what type value is because only a is affected
            elif type(target) is ast.Subscript or type(target) is ast.Slice:
                tNode: ast.Name = target.value
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
