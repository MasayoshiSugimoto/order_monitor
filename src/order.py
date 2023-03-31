
class Order:

	def __init__(self):
		self.clOrdID = None
		self.orderID = None


	def onNewOrderSingle(self, newOrderSingle):
		self.clOrdID = newOrderSingle.clOrdID()
