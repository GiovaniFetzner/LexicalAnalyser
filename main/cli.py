# main/cli.py
import argparse
from lexer.mylexer import MyLexer
from parser.myparser import MyParser
from semantic.semantic_checker import SemanticChecker
from exec.interpreter import Interpreter

def main():
    arg = argparse.ArgumentParser()
    arg.add_argument("arquivo")
    arg.add_argument("--tokens", action="store_true")
    arg.add_argument("--ast", action="store_true")
    arg.add_argument("--run", action="store_true")

    opts = arg.parse_args()

    with open(opts.arquivo) as f:
        code = f.read()

    lexer = MyLexer()
    parser = MyParser()
    checker = SemanticChecker()
    interp = Interpreter()

    tokens = list(lexer.tokenize(code))

    if opts.tokens:
        for t in tokens:
            print(t)
        return

    ast = parser.parse(iter(tokens))

    if opts.ast:
        print(ast)
        return

    checker.check(ast)
    interp.run(ast)

if __name__ == "__main__":
    main()
