from abc import ABC

Temp = int
TempLabel = str


class TempManager(ABC):
    tempCount = 0
    labelCount = 0

    @classmethod
    def new_temp(cls) -> Temp:
        cls.tempCount += 1
        return cls.tempCount

    @classmethod
    def new_label(cls) -> TempLabel:
        cls.labelCount += 1
        return f"lab_{cls.labelCount}"

    # TODO: Esto es necesario?
    # Si es necesario, que pasa cuando ya existe la label?
    # Parece que nada, nadie puso guards.
    @classmethod
    def named_label(cls, name: str) -> TempLabel:
        return name
