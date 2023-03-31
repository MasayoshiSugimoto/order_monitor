
class OrderCancelReject:


	def __init__(self, fields):
		self.fields = fields


	def msgType(self):
		return self.fields[0]


	def orderID(self):
		return self.fields[1]


	def clOrdID(self):
		return self.fields[2]


	def origClOrdID(self):
		return self.fields[3]


	def ordStatus(self):
		return self.fields[4]


	def transactTime(self):
		return self.fields[5]


	def firstClOrdID(self):
		return self.fields[6]

