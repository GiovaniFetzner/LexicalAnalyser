# lexer/mylexer.py
from sly import Lexer

class MyLexer(Lexer):
    tokens = {
        'IDENTIFICADOR', 'NUMBER', 'DECIMAL',
        'STRING_DOUBLE', 'STRING_SINGLE',
        'OPERATOR', 'DELIMITADOR', "DOT", "ELLIPSIS",
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE',

        "FALSE","NONE","TRUE","AND","AS","ASSERT","ASYNC","AWAIT",
        "BREAK","CLASS","CONTINUE","DEF","DEL","ELIF","ELSE","EXCEPT",
        "FINALLY","FOR","FROM","GLOBAL","IF","IMPORT","IN","IS","LAMBDA",
        "NONLOCAL","NOT","OR","PASS","RAISE","RETURN","TRY","WHILE",
        "WITH","YIELD",
    }

    ignore = ' \t\r'
    ignore_comment = r'\#.*'
    ignore_tricomment = r"(?:'''[\s\S]*?'''|\"\"\"[\s\S]*?\"\"\")"

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def find_column(self, token):
        last_cr = self.text.rfind("\n", 0, token.index)
        if last_cr < 0:
            last_cr = -1
        return token.index - last_cr

    FALSE=r"False"; NONE=r"None"; TRUE=r"True"
    AND=r"and"; AS=r"as"; ASSERT=r"assert"; ASYNC=r"async"; AWAIT=r"await"
    BREAK=r"break"; CLASS=r"class"; CONTINUE=r"continue"; DEF=r"def"
    DEL=r"del"; ELIF=r"elif"; ELSE=r"else"; EXCEPT=r"except"
    FINALLY=r"finally"; FOR=r"for"; FROM=r"from"; GLOBAL=r"global"
    IF=r"if"; IMPORT=r"import"; IN=r"in"; IS=r"is"; LAMBDA=r"lambda"
    NONLOCAL=r"nonlocal"; NOT=r"not"; OR=r"or"; PASS=r"pass"
    RAISE=r"raise"; RETURN=r"return"; TRY=r"try"; WHILE=r"while"
    WITH=r"with"; YIELD=r"yield"

    IDENTIFICADOR = r"[a-zA-Z_][a-zA-Z0-9_]*"
    DECIMAL = r"\d+\.\d+"
    NUMBER = r"\d+"
    STRING_DOUBLE = r"\"([^\\\n]|(\\.))*?\""
    STRING_SINGLE = r"\'([^\\\n]|(\\.))*?\'"

    DOT = r"\."
    ELLIPSIS = r"\.\.\."

    # Adicione tokens para operadores
    PLUS   = r'\+'
    MINUS  = r'-'
    TIMES  = r'\*'
    DIVIDE = r'/'
    
    OPERATOR = r'==|!=|<=|>=|//=|\*\*|=|\+|-|\*|/|<|>|%'
    DELIMITADOR = r"[{}();,:\[\]]"

    def error(self, t):
        print(f"\033[31mIllegal character {t.value[0]!r} at index {self.index}\033[0m")
        self.index += 1

__all__ = ["MyLexer"]
