import parser.ast_nodes as Node
import ply.yacc as yacc
from lexer.lex import tokens

# TODO: Remove this line after finishing.
import code

"""
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
"""

# flake8: noqa ANN001

start = "type_dec_block"


def p_empty(p):
    "empty :"
    pass


def p_empty_list(p):
    "empty_list : empty"
    p[0] = []


def p_type_dec_block(p):
    """
    type_dec_block : empty_list
                   | type_dec_list
    """
    p[0] = Node.TypeDecBlock(type=p[1])


def p_type_dec(p):
    "type_dec : TYPE ID EQ type"
    p[0] = Node.TypeDec(name=p[2], type=p[4])


# Non-empty type declaration list.
def p_type_dec_list(p):
    """
    type_dec_list : type_dec_list_iter
                  | type_dec_list_end
    """
    p[0] = p[1]


def p_type_dec_list_iter(p):
    "type_dec_list_iter : type_dec_list type_dec"
    p[0] = p[1]
    p[0].append(p[2])


def p_type_dec_list_end(p):
    "type_dec_list_end : type_dec"
    p[0] = [p[1]]


def p_type(p):
    """
    type : name_ty
         | record_ty
         | array_ty
    """
    p[0] = p[1]


def p_name_ty(p):
    "name_ty : ID"
    p[0] = Node.NameTy(p[1])


def p_record_ty(p):
    """
    record_ty : LBRACE empty_list RBRACE
              | LBRACE field_list RBRACE
    """
    p[0] = Node.RecordTy(fieldList=p[2])


def p_array_ty(p):
    "array_ty : ARRAY OF ID"
    p[0] = Node.ArrayTy(array=p[3])


def p_field(p):
    "field : ID COLON ID"
    p[0] = Node.Field(name=p[1], type=p[3])


# Non-empty record field list.
def p_field_list(p):
    """
    field_list : field_list_end
               | field_list_iter
    """
    p[0] = p[1]


def p_field_list_iter(p):
    "field_list_iter : field_list COMMA field"
    p[0] = p[1]
    p[0].append(p[3])


def p_field_list_end(p):
    "field_list_end : field"
    p[0] = [p[1]]


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


# Build the parser
parser = yacc.yacc()
