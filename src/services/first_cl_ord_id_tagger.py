from src.message_util import \
		consumeMessageStream, \
		isNewSingleOrder, \
		asTSV, \
		isResponse, \
		isExecutionReport
from src.business.exec_type import ExecType


clOrdIDToFirstClOrdID = {}
orderIDToFirstClOrdID = {}


def tagWithFirstClOrdID():
	consumeMessageStream(consume)


def consume(message):
	addFirstClOrdID(message)
	addOrderID(message)

	firstClOrdID = None
	if message.clOrdID() in clOrdIDToFirstClOrdID:
		firstClOrdID = clOrdIDToFirstClOrdID[message.clOrdID()]
	elif isResponse(message) and message.orderID() in orderIDToFirstClOrdID:
		firstClOrdID = orderIDToFirstClOrdID[message.orderID()]

	if firstClOrdID is not None:
		message.setFirstClOrdID(firstClOrdID)
	
	print(asTSV(message))


def addFirstClOrdID(message):
	clOrdID = getattr(message, 'clOrdID', lambda: "")()

	if isNewSingleOrder(message):
		clOrdIDToFirstClOrdID[clOrdID] = clOrdID
		return

	origClOrdID = getattr(message, 'origClOrdID', lambda: "")()

	if origClOrdID and clOrdID and origClOrdID in clOrdIDToFirstClOrdID:
		clOrdIDToFirstClOrdID[clOrdID] = clOrdIDToFirstClOrdID[origClOrdID]

	# Depending on the order, the new ack might come first.
	if isExecutionReport(message) and message.execType() == ExecType.NEW.value:
		clOrdIDToFirstClOrdID[clOrdID] = clOrdID


def addOrderID(message):
	if not isResponse(message):
		return

	clOrdID = getattr(message, 'clOrdID', lambda: "")()
	origClOrdID = getattr(message, 'origClOrdID', lambda: "")()
	orderID = message.orderID()
	if origClOrdID in clOrdIDToFirstClOrdID:
		orderIDToFirstClOrdID[orderID] = clOrdIDToFirstClOrdID[origClOrdID]
	elif clOrdID in clOrdIDToFirstClOrdID:
		orderIDToFirstClOrdID[orderID] = clOrdIDToFirstClOrdID[clOrdID]

    


