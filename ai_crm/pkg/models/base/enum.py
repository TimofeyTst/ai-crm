from enum import Enum

class BaseEnum(Enum):
    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return str(self.value)
