import sys
from ..message_util import createMessage


def generateClOrdIDMap():
	for line in sys.stdin:
		if len(line.strip()) == 0:
			continue
		message = createMessage(line.replace("\n", ""))
		clOrdID = getattr(message, 'clOrdID', lambda: "")()
		origClOrdID = getattr(message, 'origClOrdID', lambda: clOrdID)()
		if not clOrdID or not origClOrdID:
			continue
		print(f'{clOrdID}	{origClOrdID}')



