
from enum import Enum


class MsgType(Enum):
	EXECUTION_REPORT = '8'
	ORDER_CANCEL_REJECT = '9'
	NEW_ORDER_SINGLE = 'D'
	ORDER_CANCEL = 'F'
	ORDER_CANCEL_REPLACE = 'G'
