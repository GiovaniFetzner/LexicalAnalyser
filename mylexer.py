import ply.lex as lex

class PythonLikeLexer:

    # ---------------------------
    # Palavras-chave do Python
    # ---------------------------
    keywords = (
        'False', 'None', 'True',
        'and', 'as', 'assert', 'async', 'await',
        'break', 'class', 'continue', 'def', 'del',
        'elif', 'else', 'except', 'finally', 'for',
        'from', 'global', 'if', 'import', 'in',
        'is', 'lambda', 'nonlocal', 'not', 'or',
        'pass', 'raise', 'return', 'try', 'while', 'with', 'yield',
        'print',
    )

    # ---------------------------
    # Lista de tokens
    # ---------------------------
    tokens = [
        'NAME',
        'NUMBER',
        'STRING',
        'NEWLINE',
        'INDENT',
        'DEDENT',
    ] + [kw.upper() for kw in keywords]  # palavra-chave vira token separado

    # ---------------------------
    # Literais (somente caracteres únicos)
    # ---------------------------
    literals = ['+', '-', '*', '/', '=', '(', ')', ':', ',', '.', '<', '>']

    # ---------------------------
    # Ignorar comentários e espaços
    # ---------------------------
    t_ignore_COMMENT = r'\#.*'
    t_ignore = ' \t'

    # ---------------------------
    # Inicialização
    # ---------------------------
    def __init__(self):
        self.indent_stack = [0]  # pilha de indentação
        self.pending = []        # tokens pendentes (DEDENT)
        self.lexer = lex.lex(module=self)

    # ---------------------------
    # Tokens básicos
    # ---------------------------
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'(\".*?\"|\'.*?\')'
        return t

    # ---------------------------
    # Nome / palavra-chave
    # ---------------------------
    def t_NAME(self, t):
        r'[A-Za-z_][A-Za-z0-9_]*'
        if t.value in self.keywords:
            t.type = t.value.upper()  # converte para token da keyword
        return t

    # ---------------------------
    # NEWLINE → calcula indentação
    # ---------------------------
    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
        t.value = '\n'

        # Próxima posição na linha
        line_pos = t.lexer.lexpos
        spaces = 0
        while line_pos < len(t.lexer.lexdata) and t.lexer.lexdata[line_pos] == ' ':
            spaces += 1
            line_pos += 1

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

    # ---------------------------
    # Cria token auxiliar
    # ---------------------------
    def _make_token(self, base, type_):
        tok = lex.LexToken()
        tok.type = type_
        tok.value = None
        tok.lineno = base.lineno
        tok.lexpos = base.lexpos
        return tok

    # ---------------------------
    # Retorna token (inclui tokens pendentes)
    # ---------------------------
    def token(self):
        if self.pending:
            return self.pending.pop(0)
        return self.lexer.token()

    # ---------------------------
    # Erro
    # ---------------------------
    def t_error(self, t):
        print(f"Illegal character {t.value[0]!r} at line {t.lineno}")
        t.lexer.skip(1)
