from abc import ABC
from typing import List

from dataclasses import dataclass

from activation_records.temp import TempLabel, TempManager
from intermediate_representation.level import Access, outermost_level, RealLevel
from semantic_analysis.table import SymbolTable
from semantic_analysis.types import Type, IntType, StringType, VoidType


class EnvironmentEntry(ABC):
    pass


@dataclass
class VariableEntry(EnvironmentEntry):
    access: Access
    type: Type
    is_editable: bool = True


@dataclass
class FunctionEntry(EnvironmentEntry):
    level: RealLevel
    label: TempLabel
    formals: List[Type]
    result: Type


def base_type_environment() -> SymbolTable[Type]:
    environment = SymbolTable[Type]()
    environment.add("int", IntType())
    environment.add("string", StringType())
    return environment


def base_value_environment() -> SymbolTable[EnvironmentEntry]:
    environment = SymbolTable[EnvironmentEntry]()
    environment.add("print", base_function_entry([StringType()], VoidType()))
    environment.add("flush", base_function_entry([], VoidType()))
    environment.add("getchar", base_function_entry([], StringType()))
    environment.add("ord", base_function_entry([StringType()], IntType()))
    environment.add("chr", base_function_entry([IntType()], StringType()))
    environment.add("size", base_function_entry([StringType()], IntType()))
    environment.add(
        "substring",
        base_function_entry([StringType(), IntType(), IntType()], StringType()),
    )
    environment.add(
        "concat", base_function_entry([StringType(), StringType()], StringType())
    )
    environment.add("not", base_function_entry([IntType()], IntType()))
    environment.add("exit", base_function_entry([IntType()], VoidType()))
    return environment


def base_function_entry(formal_types: [Type], return_type: Type) -> FunctionEntry:
    function_label = TempManager.new_label()
    function_level = RealLevel(
        outermost_level, function_label, [False for _ in formal_types]
    )
    return FunctionEntry(function_level, function_label, formal_types, return_type)
