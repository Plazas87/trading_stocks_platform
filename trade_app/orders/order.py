from datetime import datetime
from random import randint


class Order:
    def __init__(self, ticker, buy_price, sell_price, quantity, order_id=None):
        self._timestamp = str(datetime.now())
        self._year = datetime.now().year
        self._month = datetime.now().month
        self._day = datetime.now().day
        self._hour = datetime.now().hour
        self._minute = datetime.now().minute
        self._ticker = ticker
        self._buy_price = buy_price/1 if buy_price > 0 else 0.0
        self._sell_price = sell_price/1 if sell_price > 0 else 0.0
        self._quantity = quantity if quantity > 0 else 0
        self._order_type = None
        self._trader_id = None
        self._cost = None

        self._order_id = order_id if order_id is not None else self._generates_id()
        self._trade_id = 0

    @property
    def trade_id(self):
        return self._trade_id

    @trade_id.setter
    def trade_id(self, value):
        if isinstance(value, int) and value > 0:
            self._trade_id = value

    @property
    def order_type(self):
        return self._order_type

    @order_type.setter
    def order_type(self, value):
        if isinstance(value, str):
            self._order_type = value

    @property
    def trader_id(self):
        return self._trader_id

    @trader_id.setter
    def trader_id(self, value):
        if isinstance(value, int) and value > 0:
            self._trader_id = value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        if isinstance(value, float) and value > 0:
            self._cost = value

    @property
    def order_id(self):
        return self._order_id

    @property
    def ticker(self):
        return self._ticker

    @ticker.setter
    def ticker(self, value):
        if isinstance(value, str):
            self._ticker = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if isinstance(value, int) and value > 0:
            self._quantity = value

    @property
    def buy_price(self):
        return self._buy_price

    @buy_price.setter
    def buy_price(self, value):
        if isinstance(value, float) and value >= 0:
            self._buy_price = value

    @property
    def sell_price(self):
        return self._sell_price

    @sell_price.setter
    def sell_price(self, value):
        if isinstance(value, float) and value >= 0:
            self._sell_price = value

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    @property
    def day(self):
        return self._day

    @property
    def hour(self):
        return self._hour

    @property
    def minute(self):
        return self._minute

    @property
    def timestamp(self):
        return self._timestamp

    def _generates_id(self):
        if (self.buy_price == self.sell_price) or (self.quantity == 0):
            return None

        elif self.buy_price > 0.0 and self.sell_price != 0.0:
            return None

        elif self.sell_price > 0.0 and self.buy_price != 0.0:
            return None
        else:
            return str(self.year) + \
                   str(self.month) + \
                   str(self.day) + \
                   str(self.hour) + \
                   str(self.minute) + \
                   str(randint(1, 10000))

    def __str__(self):
        return f'id: {self.order_id}, ' \
               f'timestamp: {self.timestamp}, ' \
               f'year: {self.year}, ' \
               f'month: {self.month}, ' \
               f'day: {self.day}, ' \
               f'hour: {self.month}, ' \
               f'minute: {self.minute}, ' \
               f'ticker: {self.ticker}, ' \
               f'buy_price: {self._buy_price}, ' \
               f'sell_price: {self._sell_price}, ' \
               f'quantity: {self.quantity} '


if __name__ == '__main__':
    order = Order('NFLX', 10, 0, 10)
    keys = [a for a in dir(order) if not (a.startswith('__') or a.startswith('_')) and not callable(getattr(order, a))]
    print(keys)

