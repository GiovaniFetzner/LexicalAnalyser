import sys
import subprocess
import os
from parser_ast import PythonLikeParser

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
# Lê arquivo do CLI
# -------------------------------
if len(sys.argv) < 2:
    print("Uso: python main.py <arquivo>")
    sys.exit(1)

input_file = sys.argv[1]

if not os.path.isfile(input_file):
    print(f"Arquivo não encontrado: {input_file}")
    sys.exit(1)

with open(input_file, "r") as f:
    code = f.read()


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
