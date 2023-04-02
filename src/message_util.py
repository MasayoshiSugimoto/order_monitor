from .msg_type import MsgType
import sys
from .execution_report import ExecutionReport
from .new_order_single import NewOrderSingle
from .order_cancel import OrderCancel
from .order_cancel_reject import OrderCancelReject
from .order_cancel_replace import OrderCancelReplace


def isResponse(message):
	msgType = message.msgType()
	return msgType == MsgType.EXECUTION_REPORT.value \
		or msgType == MsgType.ORDER_CANCEL_REJECT.value


def isRequest(message):
	return not isResponse(message)


def asHumanRow(message, header):
	cells = [getattr(message, column, lambda: "")() or "NULL" for column in header]
	print("	".join(cells))


def asHumanTable():
	print("MsgType	OrderID	ClOrdID	OrigClOrdID	ExecID	ExecType	OrdStatus	Symbol	Side	LeavesQty	CumQty	AvgPx	TransactTime	OrderQty	OrdType	Price FirstClOrdID")
	for line in sys.stdin:
		if len(line.strip()) == 0:
			continue
		message = createMessage(line.replace("\n", ""))
		asHumanRow(message, [
			"msgType",
			"orderID",
			"clOrdID",
			"origClOrdID",
			"execID",
			"execType",
			"ordStatus",
			"symbol",
			"side",
			"leavesQty",
			"cumQty",
			"avgPx",
			"transactTime",
			"orderQty",
			"ordType",
			"price",
            "firstClOrdID"
		])


def createMessage(line):
	fields = line.split('	')
	msgType = fields[0]
	if (msgType == MsgType.EXECUTION_REPORT.value):
		return ExecutionReport(fields)
	if (msgType == MsgType.ORDER_CANCEL_REJECT.value):
		return OrderCancelReject(fields)
	if (msgType == MsgType.NEW_ORDER_SINGLE.value):
		return NewOrderSingle(fields)
	if (msgType == MsgType.ORDER_CANCEL.value):
		return OrderCancel(fields)
	if (msgType == MsgType.ORDER_CANCEL_REPLACE.value):
		return OrderCancelReplace(fields)
	raise ValueError(f"Invalid msgType: {msgType}") 


def asTSV(message):
	return '	'.join(message.fields)


def isExecutionReport(message):
	return MsgType.EXECUTION_REPORT.value == message.msgType()


def isOrderCancelReject(message):
	return MsgType.ORDER_CANCEL_REJECT.value == message.msgType()


def isNewSingleOrder(message):
	return MsgType.NEW_ORDER_SINGLE.value == message.msgType()


def isOrderCancel(message):
	return MsgType.ORDER_CANCEL.value == message.msgType()


def isOrderCancelReplace(message):
	return MsgType.ORDER_CANCEL_REPLACE.value == message.msgType()


def consumeMessageStream(f):
	for line in sys.stdin:
		line = line.strip()
		if len(line) == 0:
			continue
		message = createMessage(line)
		f(message)
