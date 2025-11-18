from sly import Parser
from lexer.mylexer import MyLexer
from parser.ast_nodes import *

class MyParser(Parser):
    tokens = MyLexer.tokens

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
    )

    # Regra para expressões (termos + operações)
    @_('term')
    def expr(self, p):
        return p.term

    # Regra para termos (operações de adição e subtração)
    @_('term PLUS factor')
    def term(self, p):
        return BinOp(p.term, '+', p.factor)

    @_('term MINUS factor')
    def term(self, p):
        return BinOp(p.term, '-', p.factor)

    # Regra para fatores (multiplicação e divisão)
    @_('factor TIMES atom')
    def factor(self, p):
        return BinOp(p.factor, '*', p.atom)

    @_('factor DIVIDE atom')
    def factor(self, p):
        return BinOp(p.factor, '/', p.atom)

    # Regra para quando não há mais multiplicação ou divisão
    @_('atom')
    def factor(self, p):
        return p.atom

    # Regra para operações atômicas (números, strings, identificadores, etc.)
    @_('NUMBER')
    def atom(self, p):
        return Number(int(p.NUMBER))

    @_('STRING_DOUBLE')
    def atom(self, p):
        return String(p.STRING_DOUBLE[1:-1])  # Remove as aspas

    @_('IDENTIFICADOR')
    def atom(self, p):
        return Var(p.IDENTIFICADOR)

    # Regra de atribuição (IDENTIFICADOR = expr)
    @_('IDENTIFICADOR "=" expr')
    def statement(self, p):
        return Assign(p.IDENTIFICADOR, p.expr)

    # Expressões simples
    @_('expr')
    def statement(self, p):
        return p.expr

    # Regra do programa: uma lista de declarações (ou apenas uma)
    @_('statements')
    def program(self, p):
        return Program(p.statements)

    # Definição de declarações
    @_('statements statement')
    def statements(self, p):
        return p.statements + [p.statement]

    @_('statement')
    def statements(self, p):
        return [p.statement]

    # Regra para a expressão em parênteses
    @_('"(" expr ")"')
    def atom(self, p):
        return p.expr
