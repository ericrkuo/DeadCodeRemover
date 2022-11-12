import graphviz
import ast
from scalpel.cfg import CFGBuilder

cfg = CFGBuilder().build_from_file('example.py', './example.py')

# Render diagrams
dot = cfg.build_visual('png')
dot.render("diagrams/cfg_diagram", view=False)


for (block_id, fun_name), fun_cfg in cfg.functioncfgs.items():
    if fun_name == "fib":
        graph = fun_cfg.build_visual('png')
        graph.render("diagrams/fig_cfg", view=False) 


# Visitor method to just show features of scalpel.cfg
def visit_blocks(block, indent="", visited=[], calls=True):
        # Don't visit blocks twice.
        if block.id in visited:
            return

        print(f'{indent} Visiting block {block.id}')
        
        
        if (block.get_calls()):
            print(f'{indent}  Block makes function calls {block.get_calls().strip()}')

        print(f'{indent}  Block has {len(block.statements)} statements without control jumps')
        print(f'{indent}  Block has {len(block.exits)} exits with control jumps')
        print(f'{indent}  Code:\n')
        print(indent + '  ' + block.get_source().replace("\n", "\n"+indent+'  '))

        visited.append(block.id)

        # visit CFGs for other functions
        for statement in block.statements:
            if type(statement) is ast.FunctionDef:
                fun_cfg = next(fun_cfg for (_, fun_name), fun_cfg in cfg.functioncfgs.items() if fun_name=="fib")
                if fun_cfg:
                    print(f'{indent}  Exploring CFG for function {statement.name}')
                    visit_blocks(fun_cfg.entryblock, indent + "  ", visited, calls=calls)


        # Recursively visit all the blocks of the CFG.
        for exit in block.exits:
            visit_blocks(exit.target, indent + "  ", visited, calls=calls)

visit_blocks(cfg.entryblock)

for _, fun_cfg in cfg.functioncfgs.items():
    visit_blocks(fun_cfg.entryblock)