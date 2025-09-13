from sly import Lexer

class MyLexer(Lexer):
    tokens = {
        'DEF', 'IF', 'ELIF', 'ELSE', 'WHILE', 'RETURN', 'PRINT',
        'IDENTIFICADOR', 'NUMBER', 'DECIMAL', 'STRING_DOUBLE', 'STRING_SINGLE',
        'OPERATOR', 'DELIMITADOR', 'FROM', 'IMPORT', 'CLASS'
    }

    # ignora espaços, tabulação, quebras de linha e comentários
    ignore = ' \t\r\n'
    ignore_comment = ignore_comments = r'(?:\#.*\n)+|("""|\'\'\')(?:.|\n)*?\2'    # <- Pula os comentários até o \n

    def find_column(self, token):
        last_cr = self.text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = -1
        return token.index - last_cr

    # ----------- Palavras reservadas -----------
    DEF    = r'def'
    IF     = r'if'
    ELIF   = r'elif'
    ELSE   = r'else'
    WHILE  = r'while'
    RETURN = r'return'
    PRINT  = r'print'
    FROM = r'from'
    IMPORT = r'import'
    CLASS = r'class'

    # ----------- Tokens gerais -----------
    IDENTIFICADOR = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Número decimal (vem antes de NUMBER para ter prioridade)
    DECIMAL = r'\d+\.\d+'

    # Número inteiro
    NUMBER  = r'\d+'

    # Strings entre aspas duplas (com escapes básicos)
    STRING_DOUBLE = r'\"([^\\\n]|(\\.))*?\"'

    # Strings entre aspas simples (com escapes básicos)
    STRING_SINGLE = r'\'([^\\\n]|(\\.))*?\''

    OPERATOR    = r'==|=|\+|-|\*|/|<|>'
    DELIMITADOR = r'[{}();,:\[\]]'

    def error(self, t):
        # Texto em vermelho
        print(f"\033[31mIllegal character {t.value[0]!r} at index {self.index}\033[0m")
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

    # Ajustar valor sem aspas no caso de STRING
    lexema = token.value
    if token.type in ('STRING_DOUBLE', 'STRING_SINGLE'):
        lexema = lexema[1:-1]  # remove aspas externas
    elif token.type == 'NUMBER':
        lexema = int(lexema)
    elif token.type == 'DECIMAL':
        lexema = float(lexema)

    return (f"Token('{token.type}', lexema = '{lexema}'), "
            f"linha = {linha}, coluna = {coluna}, "
            f"inicio = {token.index}, fim = {token.end}")


# ------------------- Testando -------------------
lexer = MyLexer()

with open("arquivoTeste.py", "r", encoding="utf-8") as f:
    codigo = f.read()

# Cabeçalho da tabela
print(f"{'Tipo':<15} | {'Lexema':<30} | {'Linha':<5} | {'Coluna':<6} | {'Inicio':<6} | {'Fim':<6}")
print("-" * 80)

# Iterando pelos tokens
for token in lexer.tokenize(codigo):
    linha, coluna = local_line_info(codigo, token)  # obtém linha e coluna
    lexema = token.value

    # Ajusta valor do lexema de acordo com o tipo
    if token.type == 'STRING':
        lexema = lexema[1:-1]  # remove aspas externas
    elif token.type == 'NUMBER':
        lexema = int(lexema)
    elif token.type == 'DECIMAL':
        lexema = float(lexema)

    # Imprime uma linha da tabela
    print(f"{token.type:<15} | {str(lexema):<30} | {linha:<5} | {coluna:<6} | {token.index:<6} | {token.end:<6}")