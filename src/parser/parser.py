'''
    decs : decs dec | dec

    dec : tdec | fdec | vdec

    tdec : TYPE ID EQ type

    type : ID | rec_fields | array_def

    rec_fields : LBRACE tfields RBRACE | LBRACE RBRACE

    array_def : ARRAY OF ID

    tfields : type_field | tfields COMMA type_field

    type_field : ID COLON ID

    fdec : FUNCTION ID LPAREN RPAREN EQ exp
         | FUNCTION ID LPAREN tfields RPAREN EQ exp
         | FUNCTION ID LPAREN RPAREN COLON ID EQ exp
         | FUNCTION ID LPAREN tfields RPAREN COLON ID EQ exp

    vdec : VAR ID ASSIGN exp | VAR ID COLON ID ASSIGN exp

    exp : const
        | seqexp
        | call
        | record
        | opexp
        | flow
        | lval
        | array
        | assign
        | let

    const : integer | string | nil
    integer : INT
    string : STRING
    nil : NIL

    seqexp : LPAREN exp_seq RPAREN
    exp_seq : exp | exp_seq SEMICOLON exp

    call : ID LPAREN RPAREN | ID LPAREN args RPAREN
    args : args COMMA exp | exp

    record : ID LBRACE RBRACE | ID LBRACE content RBRACE
    content : ID EQ exp | content COMMA ID EQ exp

    opexp : MINUS exp
    | exp PLUS exp
    | exp MINUS exp
    | exp TIMES exp
    | exp DIVIDE exp
    | exp EQ exp
    | exp NEQ exp
    | exp LT exp
    | exp LE exp
    | exp GT exp
    | exp GE exp
    | exp AND exp
    | exp OR exp

    flow : BREAK
         | WHILE exp DO exp
         | IF exp THEN exp
         | IF exp THEN exp ELSE exp
         | FOR IS ASSIGN exp TO exp DO exp

    lval : var
    var : ID | ID opt_var
    opt_var : DOT ID
            | DOT ID opt_var
            | LPAREN exp RPAREN
            | LPAREN exp RPAREN opt_var

    array : ID LBRACK exp RBRACK OF exp

    assign : var ASSIGN exp

    let : LET decs IN END
        | LET decs IN exp_seq END
'''
