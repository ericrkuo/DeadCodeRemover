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
