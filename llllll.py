from sly import Lexer
class FFFMyLexer(Lexer):
    tokens = {
        # léxicos “gerais”
        'IDENTIFICADOR', 'NUMBER', 'DECIMAL',
        'STRING_DOUBLE', 'STRING_SINGLE',
        'OPERATOR', 'DELIMITADOR',"DOT", "ELLIPSIS",
        
        #Keywords
        "FALSE",
        "NONE",
        "TRUE",
        "AND",
        "AS",
        "ASSERT",
        "ASYNC",
        "AWAIT",
        "BREAK",
        "CLASS",
        "CONTINUE",
        "DEF",
        "DEL",
        "ELIF",
        "ELSE",
        "EXCEPT",
        "FINALLY",
        "FOR",
        "FROM",
        "GLOBAL",
        "IF",
        "IMPORT",
        "IN",
        "IS",
        "LAMBDA",
        "NONLOCAL",
        "NOT",
        "OR",
        "PASS",
        "RAISE",
        "RETURN",
        "TRY",
        "WHILE",
        "WITH",
        "YIELD",
    }
    # ignora espaços, tabulação, quebras de linha e comentários
    ignore = ' \t\r'
    ignore_comment = r'\#.*'
    ignore_tricomment = r"(?:'''[\s\S]*?'''|\"\"\"[\s\S]*?\"\"\")"

    # atualiza o contador de linhas
    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def find_column(self, token):
        last_cr = self.text.rfind("\n", 0, token.index)
        if last_cr < 0:
            last_cr = -1
        return token.index - last_cr

    # ----------- Palavras reservadas -----------
    FALSE = r"False"
    NONE = r"None"
    TRUE = r"True"
    AND = r"and"
    AS = r"as"
    ASSERT = r"assert"
    ASYNC = r"async"
    AWAIT = r"await"
    BREAK = r"break"
    CLASS = r"class"
    CONTINUE = r"continue"
    DEF = r"def"
    DEL = r"del"
    ELIF = r"elif"
    ELSE = r"else"
    EXCEPT = r"except"
    FINALLY = r"finally"
    FOR = r"for"
    FROM = r"from"
    GLOBAL = r"global"
    IF = r"if"
    IMPORT = r"import"
    IN = r"in"
    IS = r"is"
    LAMBDA = r"lambda"
    NONLOCAL = r"nonlocal"
    NOT = r"not"
    OR = r"or"
    PASS = r"pass"
    RAISE = r"raise"
    RETURN = r"return"
    TRY = r"try"
    WHILE = r"while"
    WITH = r"with"
    YIELD = r"yield"

    # ----------- Tokens gerais -----------
    IDENTIFICADOR = r"[a-zA-Z_][a-zA-Z0-9_]*"

    # Número decimal (vem antes de NUMBER para ter prioridade)
    DECIMAL = r"\d+\.\d+"

    # Número inteiro
    NUMBER = r"\d+"

    # Strings entre aspas duplas (com escapes básicos)
    STRING_DOUBLE = r"\"([^\\\n]|(\\.))*?\""

    # Strings entre aspas simples (com escapes básicos)
    STRING_SINGLE = r"\'([^\\\n]|(\\.))*?\'"
    
    # Identificacao do ponto para import de modulos e para Ellipsis
    DOT = r"\."
    ELLIPSIS = r"\.\.\."

    OPERATOR = r'==|!=|<=|>=|//=|\*\*|=|\+|-|\*|/|<|>|%'
    DELIMITADOR = r"[{}();,:\[\]]"

    def error(self, t):
        # Texto em vermelho
        print(f"\033[31mIllegal character {t.value[0]!r} at index {self.index}\033[0m")
        self.index += 1

# ---------------- Funções auxiliares ----------------

def local_line_info(texto, token):
    """
    Calcula linha e coluna do token no texto.
    """
    trecho = texto[: token.index]
    linha = trecho.count("\n") + 1
    if "\n" in trecho:
        coluna = token.index - trecho.rfind("\n")
    else:
        coluna = token.index + 1
    return linha, coluna

def format_token(token, lexer, texto):
    linha, coluna = local_line_info(texto, token)

    # Ajustar valor sem aspas no caso de STRING
    lexema = token.value
    if token.type in ("STRING_DOUBLE", "STRING_SINGLE"):
        lexema = lexema[1:-1]  # remove aspas externas
    elif token.type == "NUMBER":
        lexema = int(lexema)
    elif token.type == "DECIMAL":
        lexema = float(lexema)

    return (
        f"Token('{token.type}', lexema = '{lexema}'), "
        f"linha = {linha}, coluna = {coluna}, "
        f"inicio = {token.index}, fim = {token.end}"
    )

# ------------------- Testando -------------------
lexer = eeeeee()

with open("MaquinaBebida.py", "r", encoding="utf-8") as f:
    codigo = f.read()

# Cabeçalho da tabela
print(
    f"{'Tipo':<15} | {'Lexema':<30} | {'Linha':<5} | {'Coluna':<6} | {'Inicio':<6} | {'Fim':<6}"
)
print("-" * 80)

# Iterando pelos tokens
for token in lexer.tokenize(codigo):
    linha, coluna = local_line_info(codigo, token)  # obtém linha e coluna
    lexema = token.value

    # Ajusta valor do lexema de acordo com o tipo
    if token.type in ('STRING_DOUBLE', 'STRING_SINGLE'):
        lexema = lexema[1:-1]  # remove aspas externas
    elif token.type == "NUMBER":
        lexema = int(lexema)
    elif token.type == "DECIMAL":
        lexema = float(lexema)

    # Imprime uma linha da tabela
    print(
        f"{token.type:<15} | {str(lexema):<30} | {linha:<5} | {coluna:<6} | {token.index:<6} | {token.end:<6}"
    )