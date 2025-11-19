# parser_ast.py
from ply import yacc
from mylexer import PythonLikeLexer
import uuid

# ---------------------------
# NÓS DA AST
# ---------------------------
class ASTNode:
    def __init__(self, type_, value=None):
        self.id = str(uuid.uuid4())
        self.type = type_
        self.value = value
        self.error = False  # indica erro do parser
        self.children = []

    def add(self, node):
        if node is not None:
            self.children.append(node)
        return self

# ---------------------------
# Parser
# ---------------------------
class PythonLikeParser:
    tokens = PythonLikeLexer.tokens + list(PythonLikeLexer.literals)

    # Definição de precedência para evitar shift/reduce
    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
    )

    def __init__(self):
        self.lexer = PythonLikeLexer()
        self.parser = yacc.yacc(module=self)

    # -----------------------
    # Programa e statements
    # -----------------------
    def p_program(self, p):
        """program : statements"""
        p[0] = ASTNode('program')
        for stmt in p[1]:
            p[0].add(stmt)

    def p_statements_multiple(self, p):
        """statements : statements statement"""
        p[0] = p[1]
        p[0].append(p[2])

    def p_statements_single(self, p):
        """statements : statement"""
        p[0] = [p[1]]

    # Permitir NEWLINE isolado (ex.: final de arquivo ou múltiplas linhas vazias)
    def p_statements_newline(self, p):
        """statements : statements NEWLINE"""
        p[0] = p[1]

    # -----------------------
    # Statements
    # -----------------------
    def p_statement_assign(self, p):
        """statement : NAME '=' expression NEWLINE"""
        node = ASTNode('assign')
        node.add(ASTNode('var', p[1]))
        node.add(p[3])
        p[0] = node

    def p_statement_print(self, p):
        """statement : PRINT '(' expression ')' NEWLINE"""
        node = ASTNode('print')
        node.add(p[3])
        p[0] = node

    def p_statement_if(self, p):
        """statement : IF expression ':' NEWLINE INDENT statements DEDENT"""
        node = ASTNode('if')
        node.add(p[2])
        block = ASTNode('block')
        for stmt in p[6]:
            block.add(stmt)
        node.add(block)
        p[0] = node

    def p_statement_if_else(self, p):
        """statement : IF expression ':' NEWLINE INDENT statements DEDENT ELSE ':' NEWLINE INDENT statements DEDENT"""
        node = ASTNode('if_else')
        node.add(p[2])
        if_block = ASTNode('block')
        for stmt in p[6]:
            if_block.add(stmt)
        node.add(if_block)
        else_block = ASTNode('block')
        for stmt in p[12]:
            else_block.add(stmt)
        node.add(else_block)
        p[0] = node

    def p_statement_while(self, p):
        """statement : WHILE expression ':' NEWLINE INDENT statements DEDENT"""
        node = ASTNode('while')
        node.add(p[2])
        block = ASTNode('block')
        for stmt in p[6]:
            block.add(stmt)
        node.add(block)
        p[0] = node

    # -----------------------
    # Expressões
    # -----------------------
    def p_expression_binop(self, p):
        """expression : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression"""
        node = ASTNode('binop', p[2])
        node.add(p[1])
        node.add(p[3])
        p[0] = node

    def p_expression_number(self, p):
        """expression : NUMBER"""
        p[0] = ASTNode('number', p[1])

    def p_expression_name(self, p):
        """expression : NAME"""
        p[0] = ASTNode('var', p[1])

    def p_statement_newline(self, p):
        """statement : NEWLINE"""
        # apenas ignora linhas vazias
        p[0] = None

    # -----------------------
    # Erro
    # -----------------------
    def p_error(self, p):
        GREEN = '\033[38;2;8;126;108m'
        RESET = '\033[0m'
        self.error = True

        if p:
            print(f"{GREEN}Erro no parser: token não esperado{RESET}")
            print(f"{GREEN}  Tipo: {p.type}{RESET}")
            print(f"{GREEN}  Valor: {p.value!r}{RESET}")
            print(f"{GREEN}  Linha: {p.lineno}{RESET}")
            print(f"{GREEN}  Posição: {p.lexpos}{RESET}")
            rest = p.lexer.lexdata[p.lexpos:p.lexpos + 20]
            print(f"{GREEN}  Resto da linha: {rest!r}{RESET}")
        else:
            print(f"{GREEN}Erro no parser: final inesperado do arquivo{RESET}")

    # -----------------------
    # Parse
    # -----------------------
    def parse(self, code):
        return self.parser.parse(code, lexer=self.lexer.lexer)
