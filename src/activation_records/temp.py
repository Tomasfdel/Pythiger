from abc import ABC

Temp = int
TempLabel = str


class TempManager(ABC):
    temp_count = 0
    label_count = 0

    @classmethod
    def new_temp(cls) -> Temp:
        cls.temp_count += 1
        return cls.temp_count

    @classmethod
    def new_label(cls) -> TempLabel:
        cls.label_count += 1
        return f"lab_{cls.label_count}"

    # TODO: Esto es necesario?
    # Si es necesario, que pasa cuando ya existe la label?
    # Parece que nada, nadie puso guards.
    @classmethod
    def named_label(cls, name: str) -> TempLabel:
        return name
