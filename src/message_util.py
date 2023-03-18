from .msg_type import MsgType
import sys
from .execution_report import ExecutionReport
from .new_order_single import NewOrderSingle
from .order_cancel import OrderCancel
from .order_cancel_reject import OrderCancelReject
from .order_cancel_replace import OrderCancelReplace


def isResponse(message):
	msgType = message.msgType()
	return msgType == msg_type.EXECUTION_REPORT.value \
		or msgType == msg_type.ORDER_CANCEL_REJECT.value


def isRequest(message):
	return not isResponse(message)


def asHumanRow(message, header):
	cells = [getattr(message, column, lambda: "")() or "NULL" for column in header]
	print("	".join(cells))


def asHumanTable():
	print("MsgType	OrderID	ClOrdID	OrigClOrdID	ExecID	ExecType	OrdStatus	Symbol	Side	LeavesQty	CumQty	AvgPx	TransactTime	OrderQty	OrdType	Price")
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
			"price"
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

