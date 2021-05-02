from semantic_analysis.analyzers import translate_expression, SemanticError
from semantic_analysis.environment import base_type_environment, base_value_environment
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

    # Semantic Analysis
    try:
        analysed_program = translate_expression(
            base_value_environment(), base_type_environment(), parsed_program
        )
    except SemanticError as err:
        print(err)
        return

    print("All good!")
    print(analysed_program)


if __name__ == "__main__":
    main()
