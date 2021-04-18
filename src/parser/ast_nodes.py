from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass


# TODO: Use @ dataclass
# TODO: Try to use python lists. [] es feliz. null pointer no es feliz.


@dataclass
class Position:
    lineNumber: int


class ASTNode:
    pass


class Type(ASTNode):
    pass


# class ASTNode(ABC):
# @abstractmethod
# def pretty_print(self):
#     pass


@dataclass
class Field(ASTNode):
    name: str
    type: str


class Declaration(ASTNode):
    pass


@dataclass
class TypeDec(ASTNode):
    name: str
    type: Type


@dataclass
class TypeDecBlock(Declaration):
    type: [TypeDec]


@dataclass
class NameTy(Type):
    name: str


@dataclass
class RecordTy(Type):
    fieldList: [Field]


@dataclass
class ArrayTy(Type):
    array: str


# class Variable(ASTNode):
#     pass


# class SimpleVar(Variable):
#     def __init__(self, position=-1, symbol):
#         self.position = position
#         self.symbol = symbol


# class FieldVar(Variable):
#     def __init__(self, position=-1, variable, symbol):
#         self.position = position
#         self.variable = variable
#         self.symbol = symbol


# class SubscriptVar(Variable):
#     def __init__(self, position=-1, variable, expression):
#         self.position = position
#         self.variable = variable
#         self.expression = expression


# class Expression(ASTNode):
#     pass


# class VarExp(Expression):
#     def __init__(self, position=-1, variable):
#         self.position = position
#         self.variable = variable


# class NilExp(Expression):
#     def __init__(self, position):
#         self.position = position


# class IntExp(Expression):
#     def __init__(self, position=-1, integer):
#         self.position = position
#         self.integer = integer


# class StringExp(Expression):
#     def __init__(self, position=-1, string):
#         self.position = position
#         self.string = string


# class CallExp(Expression):
#     def __init__(self, position=-1, function, arguments):
#         self.position = position
#         self.function = function
#         self.arguments = arguments


# class OpExp(Expression):
#     def __init__(self, position=-1, operator, left, right):
#         self.position = position
#         self.operator = operator
#         self.left = left
#         self.right = right


# class RecordExp(Expression):
#     def __init__(self, position=-1, _type, fields):
#         self.position = position
#         self.type = _type
#         self.fields = fields


# class SeqExp(Expression):
#     def __init__(self, position=-1, sequence):
#         self.position = position


# class AssignExp(Expression):
#     def __init__(self, position=-1, variable, expression):
#         self.position = position
#         self.variable = variable
#         self.expression = expression


# class IfExp(Expression):
#     def __init__(self, position=-1, test, then, elsee):
#         self.position = position
#         self.test = test
#         self.then = then
#         self.elsee = elsee  # TODO: Por Dios encontremos un nombre mejor.


# class WhileExp(Expression):
#     def __init__(self, position=-1, test, body):
#         self.position = position
#         self.test = test
#         self.body = body


# class BreakExp(Expression):
#     def __init__(self, position):
#         self.position = position


# class ForExp(Expression):
#     def __init__(self, position=-1, variable, low, high, body):
#         self.position = position
#         self.variable = variable
#         self.low = low
#         self.high = high
#         self.body = body


# class LetExp(Expression):
#     def __init__(self, position=-1, declarations, body):
#         self.position = position
#         self.declarations = declarations
#         self.body = body


# class ArrayExp(Expression):
#     def __init__(self, position=-1, _type, size, init):
#         self.position = position
#         self.type = _type
#         self.size = size
#         self.init = init


# class Declaration(ASTNode):
#     pass


# class FunctionDec(Declaration):
#     def __init__(self, position=-1, function):
#         self.position = position
#         self.function = function


# class VarDec(Declaration):
#     def __init__(self, position=-1, symbol, _type, init):
#         self.position = position
#         self.symbol = symbol
#         self.type = _type
#         self.init = init


# class TypeDec(Declaration):
#     def __init__(self, position=-1, _type):
#         self.position = position
#         self.type = _type


# class Type(ASTNode):
#     pass


# class NameTy(Type):
#     def __init__(self, position=-1, name):
#         self.position = position
#         self.name = name


# class RecordTy(Type):
#     def __init__(self, position=-1, variable, _type, init):
#         self.position = position
#         self.variable = variable
#         self.type = _type
#         self.init = init


# class ArrayTy(Type):
#     def __init__(self, position=-1, array):
#         self.position = position
#         self.array = array


# # Que garlopa son estas clases???
# class Field(ASTNode):
#     def __init__(self, position=-1, name, _type):
#         self.position = position
#         self.name = name
#         self.type = _type


# # TODO: Todas las listas tienen la misma pinta, vale la pena que sean
# # clases diferentes?
# class FieldList(ASTNode):
#     def __init__(self, head, tail):
#         self.head = head
#         self.tail = tail


# class ExpList(ASTNode):
#     def __init__(self, head, tail):
#         self.head = head
#         self.tail = tail


# class Fundec(ASTNode):
#     def __init__(self, position=-1, name, parameters, result, body):
#         self.position = position
#         self.name = name
#         self.parameters = parameters
#         self.result = result
#         self.body = body


# class FundecList(ASTNode):
#     def __init__(self, head, tail):
#         self.head = head
#         self.tail = tail


# class DecList(ASTNode):
#     def __init__(self, head, tail):
#         self.head = head
#         self.tail = tail


# class Namety(ASTNode):
#     def __init__(self, position=-1, type):
#         self.position = position
#         self.type = type


# class NametyList(ASTNode):
#     def __init__(self, head, tail):
#         self.head = head
#         self.tail = tail


# class Efield(ASTNode):
#     def __init__(self, position=-1, expression):
#         self.position = position
#         self.expression = expression


# class EfieldList(ASTNode):
#     def __init__(self, head, tail):
#         self.head = head
#         self.tail = tail


# class Oper(Enum):
#     plus = 1
#     minus = 2
#     times = 3
#     divide = 4
#     eq = 5
#     neq = 6
#     lt = 7
#     le = 8
#     gt = 9
#     ge = 10
