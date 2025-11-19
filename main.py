from mylexer import PythonLikeLexer

lexer = PythonLikeLexer()

code = """
x = 1
if x > 0:
    y = 2
    z = y + x
print(x)
"""

lexer.lexer.input(code)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
