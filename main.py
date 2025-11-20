import sys
import subprocess
import os
import argparse
from parser_ast import PythonLikeParser
from semantic_analyzer import SemanticAnalyzer  # Importe a classe SemanticAnalyzer
from mylexer import PythonLikeLexer

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
parser = argparse.ArgumentParser(description='Analisador léxico/sintático/semântico simples')
group = parser.add_mutually_exclusive_group()
group.add_argument('--tokens', action='store_true', help='Executa apenas o lexer e imprime tokens')
group.add_argument('--ast', action='store_true', help='Gera apenas a AST (arquivo DOT/PNG)')
group.add_argument('--run', action='store_true', help='Executa o pipeline completo (parser + semântica + AST)')
parser.add_argument('input_file', help='Arquivo de entrada')
args = parser.parse_args()

input_file = args.input_file

# Se nenhuma flag for informada, comportamento padrão é --run
mode_tokens = args.tokens
mode_ast = args.ast
mode_run = args.run or not (args.tokens or args.ast)

if not os.path.isfile(input_file):
    print(f"Arquivo não encontrado: {input_file}")
    sys.exit(1)

with open(input_file, "r") as f:
    code = f.read()


# -------------------------------
# Parser e AST
# -------------------------------
def run_tokens_only(code):
    lexer = PythonLikeLexer()
    lexer.lexer.input(code)
    print("Tokens:")
    while True:
        tok = lexer.token()
        if not tok:
            break
        val = repr(tok.value)
        print(f"{tok.type}\t{val}\t(lineno={tok.lineno}, pos={tok.lexpos})")


def run_ast_only(code):
    parser = PythonLikeParser()
    ast_root = parser.parse(code)
    if parser.lexer.error or parser.error or ast_root is None:
        print("Ocorreram erros no lexer ou parser. Nenhum arquivo AST será gerado.")
        return 1
    dot_code = ast_to_dot(ast_root)
    dot_file = "ast.dot"
    png_file = "ast.png"
    with open(dot_file, "w") as f:
        f.write(dot_code)
    print(f"Arquivo DOT gerado: {dot_file}")
    try:
        subprocess.run(["dot", "-Tpng", dot_file, "-o", png_file], check=True)
        print(f"Arquivo PNG gerado: {png_file}")
    except FileNotFoundError:
        print("GraphViz não encontrado. Instale o GraphViz para gerar o PNG.")
    except subprocess.CalledProcessError as e:
        print("Erro ao gerar PNG:", e)
    return 0


def run_full(code):
    parser = PythonLikeParser()
    ast_root = parser.parse(code)
    if parser.lexer.error or parser.error or ast_root is None:
        print("Ocorreram erros no lexer ou parser. Nenhum arquivo AST será gerado.")
        return 1
    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.analyze(ast_root)
    semantic_analyzer.save_symbol_table("symbol_table.json")
    dot_code = ast_to_dot(ast_root)
    dot_file = "ast.dot"
    png_file = "ast.png"
    with open(dot_file, "w") as f:
        f.write(dot_code)
    print(f"Arquivo DOT gerado: {dot_file}")
    try:
        subprocess.run(["dot", "-Tpng", dot_file, "-o", png_file], check=True)
        print(f"Arquivo PNG gerado: {png_file}")
    except FileNotFoundError:
        print("GraphViz não encontrado. Instale o GraphViz para gerar o PNG.")
    except subprocess.CalledProcessError as e:
        print("Erro ao gerar PNG:", e)
    return 0


# Executa modo selecionado
exit_code = 0
if mode_tokens:
    run_tokens_only(code)
elif mode_ast:
    exit_code = run_ast_only(code)
elif mode_run:
    exit_code = run_full(code)

sys.exit(exit_code)
