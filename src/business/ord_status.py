from enum import Enum


class OrdStatus(Enum):
    NONE = -1
    NEW = 0
    PARTIALLY_FILLED = 1
    FILLED = 2
    DONE_FOR_DAY = 3
    CANCELED = 4
    REPLACED = 5
    PENDING_CANCEL = 6
    REJECTED = 7

