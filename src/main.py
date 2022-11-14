import sys
import ast
from scalpel.cfg import CFGBuilder
from itertools import count
import re


class AddWrongTypeException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class AssignWrongTypeException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class AbstractState():
  type_map = {}
  errors = []
  
  def assign_error(self, line_num, code, exp):
      self.errors.append((line_num, code, exp))
  
  def assign_variable(self, var: ast.Name, expr: ast.expr):
      var_name = var.id
      if var_name in self.type_map:
          val_type = self.get_value_type(expr)
          if self.type_map[var_name] != val_type:
              raise AssignWrongTypeException("Assigning wrong type")
      else:
          self.type_map[var_name] = self.get_value_type(expr)
  
  def check_add_operation(self, left: ast.expr, right: ast.expr):
      left_type = self.get_value_type(left)
      right_type = self.get_value_type(right)
      
      if left_type != right_type:
          raise AddWrongTypeException("Adding wrong type")
      
      return left_type
  
  def get_value_type(self, expr: ast.expr):
      if type(expr) is ast.Constant:
          return type(expr.value)
        
      if type(expr) is ast.Name and expr.id in self.type_map:
          return self.type_map[expr.id]

      if type(expr) is ast.BinOp and type(expr.op) is ast.Add:
          return self.check_add_operation(expr.left, expr.right)
      
      # TODO: how to deal with this case
      return type(None)


def explore_statment(statement, state: AbstractState, block_code):
    # print(statement.lineno, type(statement), state.type_map)
    if type(statement) is ast.Assign:
        # print("statment is assign")
        vars = [node for node in statement.targets if type(node) is ast.Name]
        expr = statement.value
        for var in vars:
            try:
                state.assign_variable(var, expr)
            except AddWrongTypeException as add_exp:
                state.assign_error(statement.lineno, block_code, add_exp)
            except AssignWrongTypeException as assign_exp:
                state.assign_error(statement.lineno, block_code, assign_exp)
    if type(statement) is ast.Expr and type(statement.value) is ast.Call:
        # print("statment is function call")
        args = statement.value.args
        for arg in args:
            if type(arg) is ast.BinOp and type(arg.op) is ast.Add:
                try:
                    state.check_add_operation(arg.left, arg.right)
                except AddWrongTypeException as add_exp:
                    state.assign_error(statement.lineno, block_code, add_exp)

def visit_blocks(block, visited = set(), state: AbstractState = AbstractState()):
    if block.id in visited:
        return
    
    visited.add(block.id)
    
    counter = count(0)
    line_nums = [st.lineno for st in block.statements]
    line_nums.append('')
    block_with_line_num = re.sub(r'\n', lambda m: m.group(0)+str(line_nums[next(counter)]) + '  ', block.get_source())
    block_with_line_num = block_with_line_num
    # print(block_with_line_num)
    
    # visit each statements in a block
    for statement in block.statements:
        explore_statment(statement, state, block_with_line_num)
    
    # Recursively visit all the blocks of the CFG.
    for exit in block.exits:
        visit_blocks(exit.target, visited, state)
        

if __name__ == "__main__":
    args = sys.argv[1:];
    
    assert len(args) == 1
    
    filepath = args[0]
    cfg = CFGBuilder().build_from_file('cfg', filepath)

    state = AbstractState()
    visit_blocks(cfg.entryblock, state=state)
    
    for err in state.errors:
        line_num, code, exp = err
        print(f'line# {line_num}, Except: {exp}, block: {code}\n')
    