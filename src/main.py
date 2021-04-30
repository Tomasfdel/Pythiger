def main():

    # Import the lexer and parser
    from lexer import lex as le
    from parser import parser as p
    import sys
    from ply import lex

    if len(sys.argv) == 1:
        print("Fatal error. No input file detected.")
    else:
        f = open(sys.argv[1], "r")
        data = f.read()
        f.close()

        lex.input(data)

        # Tokenize.
        # while True:
        #    tok = lex.token()
        #    if not tok:
        #        break  # No more input
        #    print(tok)
        # Hay que hacer algo de esta forma lex.lexer.position = 0
        result = p.parser.parse(data, le.lexer)
        print(result)


if __name__ == "__main__":
    main()
