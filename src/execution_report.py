
class ExecutionReport:


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


	def execID(self):
		return self.fields[4]


	def execType(self):
		return self.fields[5]


	def ordStatus(self):
		return self.fields[6]


	def symbol(self):
		return self.fields[7]


	def side(self):
		return self.fields[8]


	def leavesQty(self):
		return self.fields[9]


	def cumQty(self):
		return self.fields[10]


	def avgPx(self):
		return self.fields[11]


	def transactTime(self):
		return self.fields[12]


	def firstClOrdID(self):
		return self.fields[13]

