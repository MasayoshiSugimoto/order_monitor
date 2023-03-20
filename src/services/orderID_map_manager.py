import sys
from ..message_util import createMessage


def generateOrderIDMap():
	for line in sys.stdin:
		if len(line.strip()) == 0:
			continue
		message = createMessage(line.replace("\n", ""))
		orderID = getattr(message, 'orderID', lambda: "")()
		if not orderID:
			continue

		clOrdID = getattr(message, 'clOrdID', lambda: "")()
		if clOrdID:
			print(f'{clOrdID}	{orderID}')

		origClOrdID = getattr(message, 'origClOrdID', lambda: "")()
		if origClOrdID:
			print(f'{origClOrdID}	{orderID}')



