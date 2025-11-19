import ply.lex as lex

class PythonLikeLexer:

    # -----------------------------------
    # Lista de tokens
    # -----------------------------------
    tokens = (
        'NAME',
        'NUMBER',
        'STRING',
        'NEWLINE',
        'INDENT',
        'DEDENT',
    )

    # Operadores e literais simples
    literals = ['+', '-', '*', '/', '=', '(', ')', ':', ',', '.', '<', '>']

    # -----------------------------------
    # Ignorar comentários e espaços
    # -----------------------------------
    t_ignore_COMMENT = r'\#.*'
    t_ignore = ' \t'

    def __init__(self):
        self.indent_stack = [0]       # pilha de indentação
        self.pending = []             # tokens pendentes (para DEDENT)
        self.lexer = lex.lex(module=self)

    # -----------------------------------
    # Tokens básicos
    # -----------------------------------
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_NAME(self, t):
        r'[A-Za-z_][A-Za-z0-9_]*'
        return t

    def t_STRING(self, t):
        r'(\".*?\"|\'.*?\')'
        return t

    # -----------------------------------
    # NEWLINE → calcula indentação
    # -----------------------------------
    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
        t.value = '\n'

        # Captura posição atual na linha — pega espaços do início
        line_start = t.lexer.lexdata.find('\n', t.lexpos - len(t.value)) + 1
        pos = t.lexer.lexpos

        # Conta espaços
        spaces = 0
        while pos < len(t.lexer.lexdata) and t.lexer.lexdata[pos] == ' ':
            spaces += 1
            pos += 1

        # Níveis anteriores
        last = self.indent_stack[-1]

        # INDENT
        if spaces > last:
            self.indent_stack.append(spaces)
            self.pending.append(self._make_token(t, "INDENT"))

        # DEDENT
        elif spaces < last:
            while self.indent_stack and self.indent_stack[-1] > spaces:
                self.indent_stack.pop()
                self.pending.append(self._make_token(t, "DEDENT"))

        return t

    # -----------------------------------
    # Token auxiliar
    # -----------------------------------
    def _make_token(self, base, type_):
        tok = lex.LexToken()
        tok.type = type_
        tok.value = None
        tok.lineno = base.lineno
        tok.lexpos = base.lexpos
        return tok

    # -----------------------------------
    # Manipular tokens pendentes (DEDENT)
    # -----------------------------------
    def token(self):
        if self.pending:
            return self.pending.pop(0)
        return self.lexer.token()

    # -----------------------------------
    # Erros
    # -----------------------------------
    def t_error(self, t):
        print(f"Illegal character {t.value[0]!r}")
        t.lexer.skip(1)
