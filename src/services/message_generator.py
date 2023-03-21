from src.new_order_single import NewOrderSingle
from src.msg_type import MsgType
import random
import string
from src.message_util import asTSV


ID_LENGTH=10


def generateMessages():
	for i in range(10):
		print(asTSV(generateNewOrderSingle()))


def generateNewOrderSingle():
	return NewOrderSingle([
		MsgType.NEW_ORDER_SINGLE.value,
		generateClOrdID(),
		generateSymbol(),
		generateSide(),
		generateTransactTime(),
		generateOrderQty(),
		generateOrdType(),
		generatePrice()
	])


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
	price = random.choice(range(80, 120))
	return f'{price}'
