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
