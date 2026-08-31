from enum import Enum
from typing import NamedTuple


class Flag(Enum):
    pass


class HandlerMode(Enum):
    ROOT = "ROOT"
    CONTEXT = "CONTEXT"
    ITEM = "ITEM"


class HandlerExpectedType(NamedTuple):
    value: tuple[type, ...]
    argument: tuple[type, ...]
