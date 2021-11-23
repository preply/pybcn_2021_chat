from enum import Enum


class Const(Enum):
    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value
