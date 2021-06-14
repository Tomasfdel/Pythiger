from activation_records.temp import Temp, TempLabel
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, List, Optional

Register = str


# Assembly language instruction without register assignments.
class Instruction(ABC):
    @abstractmethod
    def format(tempMap: Callable[[Temp], str]) -> str:
        pass

    # TODO: Two-address instructions BREAK THIS BE CAREFOOL MAN.
    # Check if we use any.
    def format_aux(
        line: str, listList: List[List[Any]], tempMap: Callable[[Temp], str]
    ) -> str:
        outputString = line
        prefixList = ["'s", "'d", "'j"]
        functionList = [tempMap, tempMap, str]
        for (prefix, list, function) in zip(prefixList, listList, functionList):
            for index in range(len(list)):
                outputString = outputString.replace(
                    f"{prefix}{index}", function(list[index])
                )
        return outputString


@dataclass
class Operation(Instruction):
    line: str
    source: List[Temp]
    destination: List[Temp]
    jump: Optional[List[TempLabel]]

    def format(self, tempMap: Callable[[Temp], str]) -> str:
        self.format_aux(self.line, [self.source, self.destination, self.jump], tempMap)


@dataclass
class Label(Instruction):
    line: str
    label: TempLabel

    def format(self, tempMap: Callable[[Temp], str]) -> str:
        self.format_aux(self.line, [], tempMap)


@dataclass
class Move(Instruction):
    line: str
    source: List[Temp]
    destination: List[Temp]

    def format(self, tempMap: Callable[[Temp], str]) -> str:
        self.format_aux(self.line, [self.source, self.destination], tempMap)
