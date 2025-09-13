from sly import Lexer

class MyLexer(Lexer):
    tokens = {'DEF', 'IF', 'ELSE', 'RETURN', 'PRINT',
              'IDENTIFICADOR', 'NUMBER', 'OPERATOR', 'DELIMITADOR'}
    ignore = ' \t\n\r'

    # Palavras reservadas com regex exata (SEM USAR DECORATOR)
    DEF         = r'def'
    IF          = r'if'
    ELSE        = r'else'
    RETURN      = r'return'
    PRINT       = r'print'

    # Definição de tokens apenas com regex
    IDENTIFICADOR= r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER       = r'\d+'
    OPERATOR     = r'==|=|\+|-|\*|/|<|>'
    DELIMITADOR  = r'[{}();,:\[\]]'

# ------------------- Testando com arquivo -------------------
lexer = MyLexer()

# Abrindo o arquivo
with open("arquivoTeste.py", "r") as f:
    codigo = f.read()

# Tokenizando o conteúdo do arquivo
for token in lexer.tokenize(codigo):
    print(token)