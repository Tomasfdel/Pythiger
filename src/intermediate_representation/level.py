from abc import ABC

from dataclasses import dataclass

import activation_records.frame as frame
from activation_records.temp import TempLabel, TempManager


class Level(ABC):
    pass


@dataclass
class Access:
    level: Level
    access: frame.Access


class RealLevel(Level):
    def __init__(self, parent: Level, name: TempLabel, formals: [bool]):
        self.parent = parent
        self.name = name
        self.frame = frame.Frame(name, [True] + formals)

    def formals(self) -> [Access]:
        """Returns the access of all formals, including the static link."""

        return [
            Access(self, frame_access) for frame_access in self.frame.formalParameters
        ]

    def alloc_local(self, escape: bool) -> Access:
        return Access(self, self.frame.alloc_local(escape))


class OutermostLevel(Level):
    pass


outermost_level = OutermostLevel()


def base_program_level() -> RealLevel:
    return RealLevel(outermost_level, TempManager.new_label(), [])
