from src.new_order_single import NewOrderSingle
from src.msg_type import MsgType
import random
import string
from src.message_util import *
from enum import Enum


ID_LENGTH = 10
NB_ORDERS = 10


def generateMessages():
	for i in range(NB_ORDERS):
		generator = MessageGenerator()
		while True:
			nextMessage = generator.next()
			if nextMessage is None:
				break
			print(asTSV(nextMessage))


def generateClOrdID():
	id = generateID()
	return f'clOrdID-{id}'


def generateID():
	return ''.join(random.choice(string.digits) for i in range(ID_LENGTH))


def generateSymbol():
	symbolLength = 4
	return ''.join(random.choice(string.ascii_uppercase) for i in range(symbolLength))


def generateSide():
	return random.choice(['1', '2'])


def generateTransactTime():
	return '19981231-23:59:59'


def generateOrderQty():
	orderQty = random.choice(range(1, 30))
	return f'{orderQty}'


def generateOrdType():
	return '1'


def generatePrice():
	return random.choice(range(80, 120))


def generateOrderID():
	return f'orderID-{generateID()}'


def generateExecID():
	return f'execID-{generateID()}'


def generateOrderQty():
	return random.choice(range(1, 30))


def randomRequestState():
	return random.choice([
		State.EXECUTION_REPORT,
		State.EXECUTION_REPORT,
		State.EXECUTION_REPORT,
		State.CANCEL_REPLACE,
		State.CANCEL
	])


class State(Enum):
	NEW_ORDER_SINGLE = 1
	NEW_ORDER_SINGLE_ACK = 2
	NEW_ORDER_SINGLE_REJECT = 3
	EXECUTION_REPORT = 4
	CANCEL_REPLACE = 5
	CANCEL_REPLACE_ACK = 6
	CANCEL_REPLACE_REJECT = 7
	CANCEL = 8
	CANCEL_ACK = 9
	CANCEL_REJECT = 10
	END = 11


class MessageGenerator:
	"""
	This class generate random orders.

	The sequence is as follows:
		1. New order
		2. Choice between:
			- Reject -> Done
			- Ack
		3. Choice between:
			- Execution report
			- Cancel replace then choice between:
				+ Ack
				+ Cancel reject -> Done
			- Cancel then choice between:
				+ Ack
				+ Cancel reject -> Done
		4. Go back to 3
	"""


	def __init__(self):
		self.currentClOrdID = generateClOrdID()
		self.orderID = generateOrderID()
		self.totalQuantity = generateOrderQty()
		self.cumQty = 0
		self.symbol = generateSymbol()
		self.side = generateSide()
		self.orderType = generateOrdType()
		self.price = generatePrice()
		self.totalValue = 0
		self.lastSent = None
		self.pending = None
		self.state = State.NEW_ORDER_SINGLE


	def leavesQty(self):
		return max(self.totalQuantity - self.cumQty, 0)


	def avgPx(self):
		if self.cumQty == 0:
			return None
		return self.totalValue / self.cumQty


	def isFilled(self):
		return self.cumQty == self.totalQuantity


	def newOrderSingle(self):
		return NewOrderSingle([
			MsgType.NEW_ORDER_SINGLE.value,
			generateClOrdID(),
			self.symbol,
			self.side,
			generateTransactTime(),
			f'{self.totalQuantity}',
			self.orderType,
			f'{self.price}'
		])


	def newOrderSingleReject(self):
		return ExecutionReport([
			MsgType.EXECUTION_REPORT.value,
			self.orderID,
			self.lastSent.clOrdID(),
			'',
			generateExecID(),
			'8',
			'8',
			self.symbol,
			self.side,
			f'{self.leavesQty()}',
			f'{self.cumQty}',
			'',
			generateTransactTime()
		])


	def newOrderSingleAck(self):
		return ExecutionReport([
			MsgType.EXECUTION_REPORT.value,
			self.orderID,
			self.lastSent.clOrdID(),
			'',
			generateExecID(),
			'0',
			'0',
			self.symbol,
			self.side,
			f'{self.leavesQty()}',
			f'{self.cumQty}',
			'',
			generateTransactTime()
		])


	def executionReport(self):
		if self.leavesQty() > 1:
			quantity = random.choice(range(1, self.leavesQty()))
		else:
			quantity = 1
		self.cumQty = self.cumQty + quantity
		execType = '2' if self.isFilled() else '1'
		ordStatus = '2' if self.isFilled() else '1'
		price = self.price
		self.totalValue = self.totalValue + (price * quantity)
		return ExecutionReport([
			MsgType.EXECUTION_REPORT.value,
			self.orderID,
			self.lastSent.clOrdID(),
			'',
			generateExecID(),
			execType,
			ordStatus,
			self.symbol,
			self.side,
			f'{self.leavesQty()}',
			f'{self.cumQty}',
			f'{self.avgPx()}',
			generateTransactTime()
		])


	def orderCancelReplace(self):
		self.price = generatePrice()
		self.totalQuantity = generateOrderQty()
		return OrderCancelReplace([
			MsgType.ORDER_CANCEL_REPLACE.value,
			self.lastSent.clOrdID(),
			generateClOrdID(),
			self.symbol,
			self.side,
			generateTransactTime(),
			f'{self.totalQuantity}',
			self.orderType,
			f'{self.price}'
		])


	def cancelReplaceAck(self):
		if self.leavesQty() == 0:
			ordStatus = '2'
		elif self.cumQty > 0:
			ordStatus = '1'
		else:
			ordStatus = '5'

		self.totalQuantity = int(self.pending.orderQty())
		self.price = int(self.pending.price())

		return ExecutionReport([
			MsgType.EXECUTION_REPORT.value,
			self.orderID,
			self.pending.clOrdID(),
			self.lastSent.clOrdID(),
			generateExecID(),
			'5',
			ordStatus,
			self.symbol,
			self.side,
			f'{self.leavesQty()}',
			f'{self.cumQty}',
			f'{self.avgPx()}',
			generateTransactTime()
		])


	def orderCancelReject(self):
		if self.leavesQty() == 0:
			ordStatus = '2'
		elif self.cumQty > 0:
			ordStatus = '1'
		else:
			ordStatus = '0'

		return OrderCancelReject([
			MsgType.ORDER_CANCEL_REJECT.value,
			self.orderID,
			self.pending.clOrdID(),
			self.lastSent.clOrdID(),
			ordStatus,
			generateTransactTime()
		])


	def orderCancel(self):
		return OrderCancel([
			MsgType.ORDER_CANCEL.value,
			self.lastSent.clOrdID(),
			generateClOrdID(),
			self.symbol,
			self.side,
			generateTransactTime()
		])


	def orderCancelAck(self):
		return ExecutionReport([
			MsgType.EXECUTION_REPORT.value,
			self.orderID,
			self.pending.clOrdID(),
			self.lastSent.clOrdID(),
			generateExecID(),
			'4',
			'4',
			self.symbol,
			self.side,
			f'{self.leavesQty()}',
			f'{self.cumQty}',
			'',
			generateTransactTime()
		])


	def isDone(self):
		if self.lastSent is None:
			return False

		if self.state == State.END:
			return True

		if isExecutionReport(self.lastSent) \
				and self.lastSent.execType() in ['2', '3', '4', '8', 'C']:
			return True

		if self.leavesQty() == 0:
			return True

		return False


	def next(self):
		if self.isDone():
			self.state = State.END
			return None

		if self.state == State.NEW_ORDER_SINGLE:
			self.state = random.choice([
				State.NEW_ORDER_SINGLE_ACK,
				State.NEW_ORDER_SINGLE_ACK,
				State.NEW_ORDER_SINGLE_ACK,
				State.NEW_ORDER_SINGLE_ACK,
				State.NEW_ORDER_SINGLE_REJECT
			])
			self.lastSent = self.newOrderSingle()
			return self.lastSent

		if self.state == State.NEW_ORDER_SINGLE_ACK:
			self.state = randomRequestState()
			self.lastSent = self.newOrderSingleAck()
			return self.lastSent

		if self.state == State.NEW_ORDER_SINGLE_REJECT:
			self.state = State.END
			self.lastSent = self.newOrderSingleReject()
			return self.lastSent

		if self.state == State.EXECUTION_REPORT:
			self.state = randomRequestState()
			self.lastSent = self.executionReport()
			return self.lastSent

		if self.state == State.CANCEL_REPLACE:
			self.state = random.choice([
				State.CANCEL_REPLACE_ACK,
				State.CANCEL_REPLACE_ACK,
				State.CANCEL_REPLACE_ACK,
				State.CANCEL_REPLACE_REJECT
			])
			self.pending = self.orderCancelReplace()
			return self.pending

		if self.state == State.CANCEL_REPLACE_ACK:
			self.state = randomRequestState()
			self.lastSent = self.cancelReplaceAck()
			self.pending = None
			return self.lastSent

		if self.state == State.CANCEL_REPLACE_REJECT:
			self.state = randomRequestState()
			reject = self.orderCancelReject()
			self.pending = None
			return reject

		if self.state == State.CANCEL:
			self.state = random.choice([
				State.CANCEL_ACK,
				State.CANCEL_REJECT
			])
			self.pending = self.orderCancel()
			return self.pending

		if self.state == State.CANCEL_ACK:
			self.state = State.END
			self.lastSent = self.orderCancelAck()
			return self.lastSent

		if self.state == State.CANCEL_REJECT:
			self.state = randomRequestState()
			reject = self.orderCancelReject()
			self.pending = None
			return reject

