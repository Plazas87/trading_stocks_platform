from .order import Order
from .order_components import OrderTypes


class BuyOrder(Order):
    def __init__(self, ticker, buy_price, sell_price=0, quantity=0):
        Order.__init__(self, ticker, buy_price, sell_price, quantity)
        self.order_type = OrderTypes.buy.name


if __name__ == '__main__':
    buy_order = BuyOrder('NFLX', buy_price=10, quantity=10)

