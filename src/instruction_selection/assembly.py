from activation_records.temp import Temp, Label
from abc import ABC
from dataclasses import dataclass
from typing import List, Optional


Register = str


class Instruction(ABC):
    pass


@dataclass
class Operation(Instruction):
    line: str
    source: List[Temp]
    destination: List[Temp]
    jump: Optional[List[Label]]


@dataclass
class Label(Instruction):
    line: str
    label: Label


@dataclass
class Move(Instruction):
    line: str
    source: List[Temp]
    destination: List[Temp]
