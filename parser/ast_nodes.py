# parser/ast_nodes.py
class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class String(ASTNode):
    def __init__(self, value):
        self.value = value

class Var(ASTNode):
    def __init__(self, name):
        self.name = name

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Assign(ASTNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class Print(ASTNode):
    def __init__(self, expr):
        self.expr = expr
