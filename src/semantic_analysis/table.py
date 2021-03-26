from typing import TypeVar, Generic, Optional

T = TypeVar("T")


class SymbolTable(Generic[T]):
    def __init__(self):
        self.stack = []
        self.bindings = {}

    def add(self, identifier: str, value: T):
        self.stack.append(identifier)
        self.bindings[identifier] = self.bindings.get(identifier, []) + [value]

    def find(self, identifier: str) -> Optional[T]:
        if identifier in self.bindings:
            return self.bindings[identifier][-1]
        return None

    def begin_scope(self):
        self.stack.append(None)

    def end_scope(self):
        while len(self.stack) and self.stack[-1] is not None:
            identifier = self.stack.pop(-1)
            self.bindings[identifier].pop(-1)
            if not len(self.bindings[identifier]):
                self.bindings.pop(identifier)
