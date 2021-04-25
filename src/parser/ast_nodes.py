from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass

@dataclass
class Position:
    lineNumber: int


# TODO: Run black and flake.

# TODO: Replace dummy ASTNode definiton.
# class ASTNode(ABC):
# @abstractmethod
# def pretty_print(self):
#     pass

class ASTNode:
    pass

class Declaration(ASTNode):
    pass

class Type(ASTNode):
    pass

class Expression(ASTNode):
    pass

class Variable(ASTNode):
    pass

class Oper(Enum):
    plus = 1
    minus = 2
    times = 3
    divide = 4
    eq = 5
    neq = 6
    lt = 7
    le = 8
    gt = 9
    ge = 10

# DECLARATION

@dataclass
class DeclarationBlock(ASTNode):
    declarationList: [Declaration]

@dataclass
class TypeDec(ASTNode):
    name: str
    type: Type


@dataclass
class TypeDecBlock(Declaration):
    typeDecList: [TypeDec]


@dataclass
class NameTy(Type):
    name: str


@dataclass
class Field(ASTNode):
    name: str
    type: str


@dataclass
class RecordTy(Type):
    fieldList: [Field]


@dataclass
class ArrayTy(Type):
    array: str


@dataclass
class VariableDec(Declaration):
    name: str
    type: Type # TODO: Make this optional.
    exp: Expression

@dataclass
class FunctionDec(ASTNode):
    name: str
    params: [Field]
    returnType: Type # TODO: Make this optional.
    body: Expression

@dataclass
class FunctionDecBlock(Declaration):
    fuctionDecList: [FunctionDec]

# EXPRESSION

@dataclass
class VarExp(Expression):
    var: Variable

@dataclass
class NilExp(Expression):
    position: Position

@dataclass
class IntExp(Expression):
    int: int

@dataclass
class StringExp(Expression):
    string: str

@dataclass
class CallExp(Expression):
    func: str
    args: [Expression]

@dataclass
class OpExp(Expression):
    oper: Oper
    left: Expression
    right: Expression

@dataclass
class ExpField(ASTNode):
    name: str
    exp: Expression

@dataclass
class RecordExp(Expression):
    type: str
    fields: [ExpField]


@dataclass
class SeqExp(Expression):
    seq: [Expression]


@dataclass
class AssignExp(Expression):
    var: Variable
    exp: Expression


@dataclass
class IfExp(Expression):
    test: Expression
    then: Expression
    elsee: Expression #TODO: Por YHVH encontrar un nombre mejor.


@dataclass
class WhileExp(Expression):
    test: Expression
    body: Expression


@dataclass
class BreakExp(Expression):
    position: Position



@dataclass
class ForExp(Expression):
    var: Variable
    lo: Expression
    hi: Expression
    body: Expression



@dataclass
class LetExp(Expression):
    decs: DeclarationBlock
    body: [Expression]



@dataclass
class ArrayExp(Expression):
    type: str
    size: Expression
    init: Expression

# VARIABLE

@dataclass
class SimpleVar(Variable):
    sym: str


@dataclass
class FieldVar(Variable):
    var: Variable
    sym: str

@dataclass
class SubscriptVar(Variable):
    var: Variable
    exp: Expression