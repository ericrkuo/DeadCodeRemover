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

    def __str__(self):
        prettyM = "\n".join("  {}\t{}".format(k, v) for k, v in self.M.items())
        return f'M:\n{prettyM}\nL:\n  {str(self.L)}'

    def copy(self):
        copy = AbstractState()
        copy.M = self.M.copy()
        copy.L = self.L.copy()
        return copy
    
    def isSame(self, target: AbstractState):
        # check M
        if set(self.M.keys()) != set(target.M.keys()):
            return False
        
        for key in self.M.keys():
            if self.M[key] != target.M[key]:
                return False
        
        # check L
        if len(self.L) != len(target.L):
            return False
        for s, t in zip(self.L, target.L):
            if s != t:
                return False
        
        return True
