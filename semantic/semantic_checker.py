# semantic/semantic_checker.py
from parser.ast_nodes import *

class SemanticChecker:
    def __init__(self):
        self.table = {}

    def check(self, node):
        method = f"check_{type(node).__name__}"
        if hasattr(self, method):
            return getattr(self, method)(node)
        else:
            return None

    def check_Assign(self, node):
        value_type = self.check(node.expr)
        self.table[node.name] = value_type

    def check_Number(self, node):
        return "number"

    def check_String(self, node):
        return "string"

    def check_Var(self, node):
        if node.name not in self.table:
            raise Exception(f"Variável não definida: {node.name}")
        return self.table[node.name]

    def check_BinOp(self, node):
        left = self.check(node.left)
        right = self.check(node.right)
        if left != "number" or right != "number":
            raise Exception("Operação binária só funciona com números")
        return "number"
