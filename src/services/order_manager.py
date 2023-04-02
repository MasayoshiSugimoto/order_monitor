from src.business.order import Order
from src.message_util import consumeMessageStream, isNewSingleOrder


orders = {}
newMap = {}
clOrdIDMap = {}


def manageOrder():
    order = Order()
    consumeMessageStream(consumeOrder)


def consumeOrder(message):

    if isNewSingleOrder(message):
        newMap[message.clOrdID()] = message
    else:
        # TODO
        pass





