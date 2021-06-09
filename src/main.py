from canonical.canonize import canonize_process_fragments
from semantic_analysis.analyzers import SemanticError, translate_program
from lexer import lex as le
from parser import parser as p
import sys
from ply import lex


def main():
    if len(sys.argv) == 1:
        print("Fatal error. No input file detected.")
        return

    f = open(sys.argv[1], "r")
    data = f.read()
    f.close()

    # Lexical Analysis
    lex.input(data)
    try:
        parsed_program = p.parser.parse(data, le.lexer)
    except p.SyntacticError as err:
        print(err)
        return

    # Semantic Analysis and Intermediate Representation Translation
    try:
        analysed_program = translate_program(
            parsed_program,
        )
    except SemanticError as err:
        print(err)
        return

    process_bodies = canonize_process_fragments()

    print("All good!")
    print(analysed_program.type)
    print("Process fragment amount:", len(process_bodies))


if __name__ == "__main__":
    main()
