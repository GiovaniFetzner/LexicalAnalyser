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
        ('left', 'OR'),
        ('left', 'AND'),
        ('right', 'NOT'),
        ('left', 'LT', 'GT', 'LE', 'GE', 'EQ', 'NE'),
        ('left', '+', '-'),
        ('left', '*', '/'),
    )

    def __init__(self):
        self.lexer = PythonLikeLexer()
        self.parser = yacc.yacc(module=self)
        self.error = False  # indica se houve erro no parser

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

    # -----------------------
    # Statements
    # -----------------------
    def p_statement_assign(self, p):
        """statement : NAME '=' expression opt_newline"""
        node = ASTNode('assign')
        node.add(ASTNode('var', p[1]))
        node.add(p[3])
        p[0] = node

    def p_statement_print(self, p):
        """statement : PRINT '(' expression ')' opt_newline"""
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

    def p_expression_boolean(self, p):
        """expression : TRUE
                      | FALSE"""
        p[0] = ASTNode('boolean', p[1] == 'True')

    def p_expression_string(self, p):
        """expression : STRING"""
    # Removendo as aspas ao redor da string
        p[0] = ASTNode('string', p[1][1:-1])

    def p_expression_name(self, p):
        """expression : NAME"""
        p[0] = ASTNode('var', p[1])

    def p_expression_group(self, p):
        """expression : '(' expression ')'"""
        p[0] = p[2]

    def p_expression_compare(self, p):
        """expression : expression LT expression
                      | expression GT expression
                      | expression LE expression
                      | expression GE expression
                      | expression EQ expression
                      | expression NE expression"""
        node = ASTNode('binop', p[2])
        node.add(p[1])
        node.add(p[3])
        p[0] = node

    def p_expression_logic(self, p):
        """expression : expression AND expression
                      | expression OR expression"""
        node = ASTNode('binop', p[2])
        node.add(p[1])
        node.add(p[3])
        p[0] = node

    def p_expression_not(self, p):
        """expression : NOT expression"""
        node = ASTNode('unop', p[1])
        node.add(p[2])
        p[0] = node

    def p_statement_newline(self, p):
        """statement : NEWLINE"""
        # apenas ignora linhas vazias
        p[0] = None

    def p_opt_newline(self, p):
        """opt_newline : NEWLINE
                       | """
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
        # Use o wrapper do lexer para que INDENT/DEDENT sejam emitidos corretamente
        return self.parser.parse(code, lexer=self.lexer)
