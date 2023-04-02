from src.business.side import Side
from src.business.ord_status import OrdStatus


class Order:

    def __init__(self):
        self.orderID = ''
        self.ordStatus = OrdStatus.NONE
        self.symbol = ''
        self.side = Side.NONE
        self.cumQty = 0
        self.avgPx = 0
        self.orderQty = 0
        self.ordType = 0
        self.price = 0


