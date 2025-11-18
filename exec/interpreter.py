# exec/interpreter.py
from parser.ast_nodes import *

class Interpreter:
    def __init__(self):
        self.env = {}

    def run(self, node):
        method = f"run_{type(node).__name__}"
        if hasattr(self, method):
            return getattr(self, method)(node)

        elif hasattr(node, '__dict__'):
            for k, v in node.__dict__.items():
                if isinstance(v, list):
                    for x in v:
                        self.run(x)
                elif isinstance(v, ASTNode):
                    self.run(v)

    def run_Program(self, node):
        for stmt in node.statements:
            self.run(stmt)

    def run_Number(self, node):
        return node.value

    def run_String(self, node):
        return node.value

    def run_Var(self, node):
        return self.env[node.name]

    def run_Assign(self, node):
        self.env[node.name] = self.run(node.expr)

    def run_BinOp(self, node):
        left = self.run(node.left)
        right = self.run(node.right)
        return eval(f"{left} {node.op} {right}")
