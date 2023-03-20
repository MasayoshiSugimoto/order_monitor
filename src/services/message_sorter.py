import sys
from src.message_util import *
from src.msg_type import MsgType


clOrdIDToFirstClOrdID = {}
orderSorterMap = {}


class OrderSorter:

	def __init__(self):
		self.requests = []
		self.responses = []
		self.currentClOrdID = None


	def onMessage(self, message):
		if isRequest(message):
			self.requests.append(message)
		else:
			self.responses.append(message)

		self.consume()


	def consume(self):
		while True:
			# Send the message straight away because it will always be first.
			if len(self.requests) > 0 and isNewSingleOrder(self.requests[0]):
				self.currentClOrdID = self.requests[0].clOrdID()
				print(asTSV(self.requests[0]))
				self.requests.pop(0)
				# Keep in the stack because we depop with last execution report.
				continue

			# Consume all execution for the request sent last.
			if len(self.responses) > 0:
				response = self.responses[0]
				if response.clOrdID() == self.currentClOrdID:
					self.responses.pop(0)
					print(asTSV(response))
					continue

			if len(self.responses) > 0 and len(self.requests) > 0:
				request = self.requests[0]
				response = self.responses[0]

				# For cancel requests and cancel replace request, depop by pair.
				if (isOrderCancelReplace(request) or isOrderCancel(request)) \
						and isExecutionReport(response) \
						and response.clOrdID() == request.clOrdID():
					self.currentClOrdID = request.clOrdID()
					self.requests.pop(0)
					self.responses.pop(0)
					print(asTSV(request))
					print(asTSV(response))
					continue

				if (isOrderCancelReplace(request) or isOrderCancel(request)) \
						and isOrderCancelReject(response) \
						and request.clOrdID() == response.clOrdID():
					self.requests.pop(0)
					self.responses.pop(0)
					print(asTSV(request))
					print(asTSV(response))
					continue

				if request.clOrdID() == response.clOrdID():
					self.currentClOrdID = request.clOrdID()
					self.requests.pop(0)
					print(asTSV(request))
					continue

			# If nothing could be done, wait for more messages.
			break


def sortMessages():
	for line in sys.stdin:
		if len(line.strip()) == 0:
			continue

		message = createMessage(line.replace("\n", ""))
		addFirstClOrdIDMapping(message)

		assert message.clOrdID() in clOrdIDToFirstClOrdID

		firstClOrdID = clOrdIDToFirstClOrdID[message.clOrdID()]
		if firstClOrdID not in orderSorterMap:
			orderSorter = OrderSorter()
			orderSorterMap[firstClOrdID] = orderSorter
		else:
			orderSorter = orderSorterMap[firstClOrdID]

		orderSorter.onMessage(message)


def addFirstClOrdIDMapping(message):
	clOrdID = getattr(message, 'clOrdID', lambda: "")()

	if message.msgType == MsgType.NEW_ORDER_SINGLE.value:
		clOrdIDToFirstClOrdID[clOrdID] = clOrdID
		return

	origClOrdID = getattr(message, 'origClOrdID', lambda: "")()

	if origClOrdID and clOrdID:
		clOrdIDToFirstClOrdID[clOrdID] = clOrdIDToFirstClOrdID[origClOrdID]
		return

	# We only expect first execution in case the execution arrives before
	# the new order single.
	if not origClOrdID and clOrdID not in clOrdIDToFirstClOrdID:
		clOrdIDToFirstClOrdID[clOrdID] = clOrdID



