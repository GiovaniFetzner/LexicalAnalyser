from parser_ast import PythonLikeParser
import subprocess
import os

# -------------------------------
# Função para gerar DOT
# -------------------------------
def ast_to_dot(node):
    """Gera texto DOT para GraphViz a partir de ASTNode"""
    lines = []
    lines.append('digraph AST {')
    lines.append('node [shape=box];')

    def walk(n):
        label = f"{n.type}"
        if n.value is not None:
            label += f"\\n{n.value}"
        lines.append(f'"{n.id}" [label="{label}"];')
        for child in n.children:
            lines.append(f'"{n.id}" -> "{child.id}";')
            walk(child)

    walk(node)
    lines.append('}')
    return '\n'.join(lines)


# -------------------------------
# Código exemplo
# -------------------------------
code = """
x = 1
y = 2
z = x + y
print(z)
"""

# -------------------------------
# Parser e AST
# -------------------------------
parser = PythonLikeParser()
ast_root = parser.parse(code)

# -------------------------------
# Gerar DOT
# -------------------------------
dot_code = ast_to_dot(ast_root)
dot_file = "ast.dot"
png_file = "ast.png"

with open(dot_file, "w") as f:
    f.write(dot_code)
print(f"Arquivo DOT gerado: {dot_file}")

# -------------------------------
# Gerar PNG usando GraphViz
# -------------------------------
try:
    subprocess.run(["dot", "-Tpng", dot_file, "-o", png_file], check=True)
    print(f"Arquivo PNG gerado: {png_file}")
except FileNotFoundError:
    print("GraphViz não encontrado. Instale o GraphViz para gerar o PNG.")
except subprocess.CalledProcessError as e:
    print("Erro ao gerar PNG:", e)
