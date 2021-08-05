from activation_records.frame import TempMap
from lexer import lex as le
from parser import parser as p
from ply import lex

import parser.ast_nodes as ast
from semantic_analysis.analyzers import TypedExpression, translate_program


def parse_program(file_name: str) -> ast.Expression:
    with open("examples/" + file_name, "r") as file:
        data = file.read()
    le.lexer.lineno = 1
    lex.input(data)
    return p.parser.parse(data, le.lexer)


def semantic_analysis(file_name: str) -> TypedExpression:
    TempMap.initialize()
    return translate_program(parse_program(file_name))
