from activation_records.temp import Temp, TempLabel
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, List, Optional


# Assembly language instruction without register assignments.
class Instruction(ABC):
    # Returns the instruction as a string, replacing the placeholders with temporaries.
    @abstractmethod
    def format(temp_map: Callable[[Temp], str]) -> str:
        pass

    def format_aux(
        line: str, temp_list_list: List[List[Any]], temp_map: Callable[[Temp], str]
    ) -> str:
        output_string = line
        prefix_list = ["'s", "'d", "'j"]
        function_list = [temp_map, temp_map, str]
        for (prefix, temp_list, function) in zip(
            prefix_list, temp_list_list, function_list
        ):
            for index in range(len(temp_list)):
                output_string = output_string.replace(
                    f"{prefix}{index}", function(temp_list[index])
                )
        return output_string


@dataclass
class Operation(Instruction):
    line: str
    source: List[Temp]
    destination: List[Temp]
    jump: Optional[List[TempLabel]]

    def format(self, temp_map: Callable[[Temp], str]) -> str:
        self.format_aux(self.line, [self.source, self.destination, self.jump], temp_map)


@dataclass
class Label(Instruction):
    line: str
    label: TempLabel

    def format(self, temp_map: Callable[[Temp], str]) -> str:
        self.format_aux(self.line, [], temp_map)


@dataclass
class Move(Instruction):
    line: str
    source: List[Temp]
    destination: List[Temp]

    def format(self, temp_map: Callable[[Temp], str]) -> str:
        self.format_aux(self.line, [self.source, self.destination], temp_map)


@dataclass
class Procedure:
    prologue: str
    body: List[Instruction]
    epilogue: str
