from trade_app.orders import Order


class Trade:
    def __init__(self, order, trade_id, profit, result, status, order_id=None):
        self._order = order
        self._trade_id = trade_id
        self._profit = profit/1
        self._result = result
        self._status = status

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        if isinstance(value, Order):
            self._order = value

    @property
    def trade_id(self):
        return self._trade_id

    @trade_id.setter
    def trade_id(self, value):
        if isinstance(value, int):
            self._trade_id = value

    @property
    def profit(self):
        return self._profit

    @profit.setter
    def profit(self, value):
        if isinstance(value, float):
            self._profit = value

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        if isinstance(value, str) and len(value) == 1:
            self._result = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if isinstance(value, bool):
            self._status = value
