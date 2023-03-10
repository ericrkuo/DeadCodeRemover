from __future__ import annotations
from collections import deque
import json

class AbstractState:
    '''
    The abstract state for program slicing consists of a pair (M, L).
    Please see each field for respective documentation
    '''

    def __init__(self):
        self.M = dict()
        '''M is a map from variable names to sets of integers'''

        self.L = deque()
        '''L is a list of sets of integers'''

        self.funcName = ''
        '''Name of the function being analyzed'''

    def __str__(self):
        prettyM = "\n".join("  {}\t{}".format(k, v) for k, v in self.M.items())
        return f'M:\n{prettyM}\nL:\n  {str(self.L)}'

    def copy(self):
        copy = AbstractState()
        copy.M = self.M.copy()
        copy.L = self.L.copy()
        copy.funcName = self.funcName
        return copy
    
    def __eq__(self, other: AbstractState):
        return self.M == other.M and self.L == other.L
