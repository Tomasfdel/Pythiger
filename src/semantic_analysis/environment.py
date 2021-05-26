from abc import ABC
from typing import List

from dataclasses import dataclass

from semantic_analysis.table import SymbolTable
from semantic_analysis.types import Type, IntType, StringType, VoidType


class EnvironmentEntry(ABC):
    pass


@dataclass
class VariableEntry(EnvironmentEntry):
    type: Type
    is_editable: bool = True


@dataclass
class FunctionEntry(EnvironmentEntry):
    formals: List[Type]
    result: Type


def base_type_environment() -> SymbolTable[Type]:
    environment = SymbolTable[Type]()
    environment.add("int", IntType())
    environment.add("string", StringType())
    return environment


def base_value_environment() -> SymbolTable[EnvironmentEntry]:
    environment = SymbolTable[EnvironmentEntry]()
    environment.add("print", FunctionEntry([StringType()], VoidType()))
    environment.add("flush", FunctionEntry([], VoidType()))
    environment.add("getchar", FunctionEntry([], StringType()))
    environment.add("ord", FunctionEntry([StringType()], IntType()))
    environment.add("chr", FunctionEntry([IntType()], StringType()))
    environment.add("size", FunctionEntry([StringType()], IntType()))
    environment.add(
        "substring", FunctionEntry([StringType(), IntType(), IntType()], StringType())
    )
    environment.add("concat", FunctionEntry([StringType(), StringType()], StringType()))
    environment.add("not", FunctionEntry([IntType()], IntType()))
    environment.add("exit", FunctionEntry([IntType()], VoidType()))
    return environment
