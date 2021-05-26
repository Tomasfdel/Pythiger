from abc import ABC
from enum import Enum, auto
from typing import Any, Optional

from dataclasses import dataclass

from activation_records.temp import TempLabel, Temp


class BinaryOperator(Enum):
    plus = auto()
    minus = auto()
    mul = auto()
    div = auto()
    andOp = auto()
    orOp = auto()
    lshift = auto()
    rshift = auto()
    arshift = auto()
    xor = auto()


class RelationalOperator(Enum):
    eq = auto()
    ne = auto()
    lt = auto()
    gt = auto()
    le = auto()
    ge = auto()
    ult = auto()
    ule = auto()
    ugt = auto()
    uge = auto()


class Statement(ABC):
    pass


class Expression(ABC):
    pass


@dataclass
class Sequence(Statement):
    sequence: [Statement]


@dataclass
class Label(Statement):
    label: TempLabel


@dataclass
class Jump(Statement):
    expression: Expression
    labels: [TempLabel]


@dataclass
class ConditionalJump(Statement):
    operator: RelationalOperator
    left: Expression
    right: Expression
    true: Optional[TempLabel] = None
    false: Optional[TempLabel] = None


@dataclass
class Move(Statement):
    temporary: Expression
    expression: Expression


@dataclass
class StatementExpression(Statement):
    expression: Expression


@dataclass
class BinaryOperation(Expression):
    operator: BinaryOperator
    left: Expression
    right: Expression


@dataclass
class Memory(Expression):
    expression: Expression


@dataclass
class Temporary(Expression):
    temporary: Temp


@dataclass
class EvaluateSequence(Expression):
    statement: Statement
    expression: Expression


@dataclass
class Name(Expression):
    label: TempLabel


@dataclass
class Constant(Expression):
    value: int


@dataclass
class Call(Expression):
    function: Expression
    arguments: [Expression]


# TODO: See if I can make these Any a bit more strict.
@dataclass
class Condition:
    statement: Statement
    trues: [Any]
    falses: [Any]
