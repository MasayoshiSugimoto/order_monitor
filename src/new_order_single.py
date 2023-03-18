
class NewOrderSingle:

	def __init__(self, fields):
		self.fields = fields


	def msgType(self):
		return self.fields[0]


	def clOrdID(self):
		return self.fields[1]


	def symbol(self):
		return self.fields[2]


	def side(self):
		return self.fields[3]


	def transactTime(self):
		return self.fields[4]


	def orderQty(self):
		return self.fields[5]


	def ordType(self):
		return self.fields[6]


	def price(self):
		return self.fields[7]


	def firstClOrdID(self):
		return self.fields[8]
