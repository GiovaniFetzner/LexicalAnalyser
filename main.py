from parser_ast import PythonLikeParser
from ast_to_dot import ast_to_dot

code = """
x = 1
y = 2
z = x + y
print(z)
"""

parser = PythonLikeParser()
ast_root = parser.parse(code)

dot_code = ast_to_dot(ast_root)

# Salvar .dot
with open("ast.dot", "w") as f:
    f.write(dot_code)

print("Arquivo AST gerado: ast.dot")
