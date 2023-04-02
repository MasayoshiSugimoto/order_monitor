MAX_LENGTH = 7


class OrderCancel:


	def __init__(self, fields):
		self.fields = fields
		while len(self.fields) < MAX_LENGTH:
			self.fields.append('')


	def msgType(self):
		return self.fields[0]


	def origClOrdID(self):
		return self.fields[1]


	def clOrdID(self):
		return self.fields[2]


	def symbol(self):
		return self.fields[3]


	def side(self):
		return self.fields[4]


	def transactTime(self):
		return self.fields[5]


	def firstClOrdID(self):
		return self.fields[6]


	def setFirstClOrdID(self, firstClOrdID):
		self.fields[6] = firstClOrdID
