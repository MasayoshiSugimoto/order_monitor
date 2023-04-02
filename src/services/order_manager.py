from src.business.order import Order
from src.message_util import \
        consumeMessageStream, \
        isNewSingleOrder, \
        isExecutionReport, \
        asTSV
from src.business.side import Side
from src.business.ord_status import OrdStatus


orders = {}


def manageOrder():
    consumeMessageStream(consumeOrder)


def consumeOrder(message):

    firstClOrdID = message.firstClOrdID()

    assert firstClOrdID is not None

    if isNewSingleOrder(message):
        order = Order()
        orders[firstClOrdID] = order
        order.symbol = message.symbol()
        order.side = Side(message.side())
        order.price = message.price()
        print(order.asTSV())
    elif firstClOrdID in orders:
        order = orders[firstClOrdID]

        if isExecutionReport(message):
            if not order.orderID:
                order.orderID = message.orderID()
            if message.ordStatus():
                order.ordStatus = OrdStatus(int(message.ordStatus()))
            if message.cumQty():
                order.cumQty = int(message.cumQty())
            if message.avgPx():
                if message.avgPx() == 'None':
                    print(asTSV(message))
                order.avgPx = float(message.avgPx())
            if message.cumQty() and message.leavesQty():
                order.orderQty = int(message.cumQty()) + int(message.leavesQty())

        print(order.asTSV())




