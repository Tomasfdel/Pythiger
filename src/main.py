# Import the lexer and parser
from lexer import lex as le
from parser import parser as p
import sys
from ply import lex


def main():

    if len(sys.argv) == 1:
        print("Fatal error. No input file detected.")
    else:
        f = open(sys.argv[1], "r")
        data = f.read()
        f.close()

        lex.input(data)
        try:
            result = p.parser.parse(data, le.lexer)
            print(result)
        except p.SyntacticError as err:
            print(err)


if __name__ == "__main__":
    main()
