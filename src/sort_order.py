import sys
from msg_type import MsgType
from execution_report import ExecutionReport
from new_order_single import NewOrderSingle
from order_cancel import OrderCancel
from order_cancel_reject import OrderCancelReject
from order_cancel_replace import OrderCancelReplace
from message_util import isResponse, isRequest


#class OrderSorter:
#
#	def __init__(self):
#		self.requests = []
#		self.responses = []
#		self.lastRequestSent = None
#
#
#SORTER = OrderSorter()
#
#
#def extractOrigClOrdIDLink(message):
#	if isResponse(message):
#		print(f'{message.origClOrdID()}	{message.clOrdID()}')


#def sendMessage(message):
#	if isResponse(message):
#		print(message)
#	else if SORTER.lastRequestSent != message.clOrdID():
#		print(message)
#		SORTER.lastRequestSent = message.clOrdID()
#
#
#def sortMessage(message):
#	# Send the new order single message as soon as received since it is always first.
#	if message.msgType == msgType.NEW_ORDER_SINGLE.value:
#		sendMessage(message)
#
#	if isResponse(message):
#		SORTER.responses.append(message)
#	else:
#		SORTER.requests.append(message)



def createMessage(line):
	fields = line.split('	')
	msgType = fields[0]
	print(f"'{msgType}'")
	if (msgType == MsgType.EXECUTION_REPORT.value):
		return ExecutionReport(fields)
	if (msgType == MsgType.ORDER_CANCEL_REJECT.value):
		return OrderCancelReject(fields)
	if (msgType == MsgType.NEW_ORDER_SINGLE.value):
		return NewOrderSingle(fields)
	if (msgType == MsgType.ORDER_CANCEL.value):
		return OrderCancel(fields)
	if (msgType == MsgType.ORDER_CANCEL_REPLACE.value):
		return OrderCancelReject(fields)
	raise ValueError(f"Invalid msgType: {msgType}") 


for line in sys.stdin:
	message = createMessage(line)
	print(message)
