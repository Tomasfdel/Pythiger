from typing import List
from abc import ABC
from munch import munch_statement
import instruction_selection.assembly as Assembly
import intermediate_representation.tree as IRT


class Codegen(ABC):
    instruction_list = []

    @classmethod
    def emit(cls, instruction: Assembly.Instruction) -> None:
        cls.instruction_list.append(instruction)

    @classmethod
    def codegen(cls, statement_list: List[IRT.Statement]) -> List[Assembly.Instruction]:
        for statement in statement_list:
            munch_statement(statement)
        instruction_list_copy = cls.instruction_list
        cls.instruction_list = []
        return instruction_list_copy
