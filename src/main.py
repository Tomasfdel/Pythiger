def main ():

    # Import the lexer and parser
    from lexer import lex as l
    from parser import parser as p
    import sys
    from ply import lex, yacc

    if len(sys.argv) > 1:
        f = open(sys.argv[1], "r")
        data = f.read()
        f.close()
    

    lex.input(data)

    # Tokenize
    while True:
        tok = lex.token()
        if not tok:
            break  # No more input
        print(tok)

    result = p.parser.parse(data, l.lexer)
    print(result)
    
    
if __name__ == '__main__':
    main()
