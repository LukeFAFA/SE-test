import ast
import astor
import sys
import random

class Mutator(ast.NodeTransformer):
    def visit_Compare(self, node):
        # Mutate: Negate comparison operator
        if isinstance(node.ops[0], ast.Gt):
            node.ops = [ast.Lt()]
        elif isinstance(node.ops[0], ast.Lt):
            node.ops = [ast.Gt()]
        return self.generic_visit(node)

    def visit_BinOp(self, node):
        # Mutate: Swap binary operators
        if isinstance(node.op, ast.Add):
            node.op = ast.Sub()
        elif isinstance(node.op, ast.Sub):
            node.op = ast.Add()
        elif isinstance(node.op, ast.Mult):
            node.op = ast.FloorDiv()
        elif isinstance(node.op, ast.FloorDiv):
            node.op = ast.Mult()
        return self.generic_visit(node)

# The visit_Assign method has been removed

def mutate(source_file, num_mutants):
    with open(source_file, "r") as source:
        tree = ast.parse(source.read(), filename=source_file)
    
    mutator = Mutator()

    for i in range(num_mutants):
        mutated_tree = ast.fix_missing_locations(mutator.visit(ast.parse(astor.to_source(tree))))
        with open("{}.py".format(i), "w") as mutant_file:
            mutant_file.write(astor.to_source(mutated_tree))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python mutate.py <source_file.py> <num_mutants>")
        sys.exit(1)
    
    source_file = sys.argv[1]
    num_mutants = int(sys.argv[2])

    mutate(source_file, num_mutants)
