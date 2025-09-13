from sly import Lexer

class MyLexer(Lexer):
    tokens = {
        'DEF', 'IF', 'ELSE', 'RETURN', 'PRINT',
        'IDENTIFICADOR', 'NUMBER', 'OPERATOR', 'DELIMITADOR'
    }

    ignore = ' \t\n\r'

    def __init__(self):
        super().__init__()
        self.lineno = 1

    def t_newline(self, t):
        r'\n+'
        self.lineno += t.value.count('\n')
        pass

    def find_column(self, token):
        last_cr = self.text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = -1
        return token.index - last_cr

    DEF    = r'def'
    IF     = r'if'
    ELSE   = r'else'
    RETURN = r'return'
    PRINT  = r'print'

    IDENTIFICADOR = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER        = r'\d+'
    OPERATOR      = r'==|=|\+|-|\*|/|<|>'
    DELIMITADOR   = r'[{}();,:\[\]]'

    def error(self, t):
        print(f"Illegal character {t.value[0]!r} at index {self.index}")
        self.index += 1


# ---------------- Funções auxiliares ----------------

def local_line_info(texto, token):
    """
    Calcula linha e coluna do token no texto.
    """
    trecho = texto[:token.index]
    linha = trecho.count('\n') + 1
    if '\n' in trecho:
        coluna = token.index - trecho.rfind('\n')
    else:
        coluna = token.index + 1
    return linha, coluna


def format_token(token, lexer, texto):
    linha, coluna = local_line_info(texto, token)
    return (f"Token('{token.type}', lexema = '{token.value}'), "
            f"linha = {linha}, coluna = {coluna}, "
            f"inicio = {token.index}, fim = {token.end}")


# ------------------- Testando -------------------
lexer = MyLexer()

with open("arquivoTeste.py", "r") as f:
    codigo = f.read()

for token in lexer.tokenize(codigo):
    print(format_token(token, lexer, codigo))