from enum import Enum


class ExecType(Enum):
    NEW = '0'
    PARTIAL_FILL = '1'
    FILL = '2'
    DONE_FOR_DAY = '3'
    CANCELED = '4'
    REPLACED = '5'
    PENDING_CANCEL = '6'
    STOPPED = '7'
    REJECTED = '8'
    SUSPENDED = '9'
    PENDING_NEW = 'A'
    CALCULATED = 'B'
    EXPIRED = 'C'
    RESTARTED = 'D'
    PENDING_REPLACE = 'E'


