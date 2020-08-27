from trade_app.orders import OrderComponents, OrderTypes
from trade_app.trade import TradeComponents, TradeResults, TradeStatus
from trade_app.trade import Trade
from trade_app.config.config_trade import ConfigTrade
from random import randint
from datetime import datetime


class Trader:

    def __init__(self, config_obj):
        self.platform_confirmation = False
        self._id_trader = self.generate_trader_id()
        self.max_lost_per_trade = float(config_obj[ConfigTrade.max_lost_per_trade.name])
        self.max_lost_per_day = float(config_obj[ConfigTrade.max_lost_per_day.name])
        self.max_buy_per_trade = float(config_obj[ConfigTrade.max_buy_per_trade.name])

    @property
    def id_trader(self):
        return self._id_trader

    def prepare_order(self, order):
        try:
            order.trader_id = int(self.id_trader)

            if order.order_type == OrderTypes.buy.name:
                cost = order.buy_price * order.quantity

            elif order.order_type == OrderTypes.sell.name:
                cost = order.sell_price * order.quantity

            order.cost = cost

            # order_dict = self.order_to_dict(order)

            return order

        except Exception as e:
            print(e, "Can't create the order: ", e.args)
            return False, 0

    def prepare_trade(self, order, trade_id=None):
        try:
            order = self.prepare_order(order)

            trade = Trade(order, self._generates_trade_id(), 0, TradeResults.waiting.value, TradeStatus.working.value)

            if trade_id is not None:
                order.trade_id = trade_id

            else:
                order.trade_id = int(trade.trade_id)

            order_dict = self.order_to_dict(order)
            trade_dict = self.trade_to_dict(trade)

            return True, trade_dict, order_dict
        except Exception as e:
            print(e)
            return False, {}, {}

    def execute_order(self, order_dict):
        if order_dict[OrderComponents.order_type.name] == OrderTypes.buy.name:
            try:
                print('    La orden de compra número {0} de {1} ha sido enviada a TOS'.format(order_dict[OrderComponents.order_id.name],
                                                                                              order_dict[OrderComponents.ticker.name]))

                self.platform_confirmation = True
                return self.platform_confirmation

            except Exception as e:
                print(e, '- Error in trader.py: {} method executeOrder'.format(e.__traceback__.tb_lineno))
                self.platform_confirmation = False
                return self.platform_confirmation

        elif order_dict[OrderComponents.order_type.name] == OrderTypes.sell.name:
            try:
                print('    La orden de venta número {0} de {1} ha sido enviada a TOS'.format(order_dict[OrderComponents.order_id.name],
                                                                                             order_dict[OrderComponents.ticker.name]))
                # enviar llamada a la plataforma de TOS
                return True
            except Exception as e:
                print(e, '- Error in trader.py: {} method executeOrder'.format(e.__traceback__.tb_lineno))
                return False

    @staticmethod
    def order_to_dict(order):
        order_dict = {OrderComponents.order_id.name: order.order_id,
                      OrderComponents.trade_id.name: order.trade_id,
                      OrderComponents.time_stamp.name: order.timestamp,
                      OrderComponents.year.name: order.year,
                      OrderComponents.month.name: order.month,
                      OrderComponents.day.name: order.day,
                      OrderComponents.hour.name: order.hour,
                      OrderComponents.minute.name: order.minute,
                      OrderComponents.ticker.name: order.ticker,
                      OrderComponents.buy_price.name: order.buy_price,
                      OrderComponents.sell_price.name: order.sell_price,
                      OrderComponents.quantity.name: order.quantity,
                      OrderComponents.order_type.name: order.order_type,
                      OrderComponents.trader_id.name: order.trader_id,
                      OrderComponents.cost.name: order.cost}
        return order_dict

    @staticmethod
    def print_order(order):
        for key, value in order.items():
            print(f'{key}: {value}')

    @staticmethod
    def trade_to_dict(trade):
        trade_dict = Trader.order_to_dict(trade.order)
        trade_dict[TradeComponents.trade_id.name] = trade.trade_id
        trade_dict[TradeComponents.profit.name] = trade.profit
        trade_dict[TradeComponents.result.name] = trade.result
        trade_dict[TradeComponents.status.name] = trade.status
        trade_dict[OrderComponents.order_type.name] = OrderTypes.trade.name

        return trade_dict

    @staticmethod
    def generate_trader_id():
        return str(datetime.now().day) + str(datetime.now().month) + str(datetime.now().year) + str(randint(1, 10000))

    @staticmethod
    def _generates_trade_id():
        return str(datetime.now().year) + \
               str(datetime.now().month) + \
               str(datetime.now().day) + \
               str(datetime.now().hour) + \
               str(datetime.now().minute) + \
               str(datetime.now().second) + \
               str(randint(1, 1000))

    @staticmethod
    def update_sell_price(trade_to_update, sell_price):
        trade_to_update[OrderComponents.sell_price.name] = sell_price
        return trade_to_update

    @staticmethod
    def update_profit(trade_to_update, sell_cost):
        profit = sell_cost - trade_to_update[OrderComponents.cost.name]
        trade_to_update[TradeComponents.profit.name] = profit

        return trade_to_update

    @staticmethod
    def update_quantity(trade_to_update, quantity):
        trade_to_update[OrderComponents.quantity.name] -= quantity
        return trade_to_update

    @staticmethod
    def update_result(trade):
        if trade[OrderComponents.quantity.name] == 0:

            if trade[TradeComponents.profit.name] >= 0:
                trade[TradeComponents.result.name] = TradeResults.positive.value

            else:
                trade[TradeComponents.result.name] = TradeResults.negative.value

        return trade

    @staticmethod
    def update_status(trade):
        if trade[OrderComponents.quantity.name] == 0:
            trade[TradeComponents.status.name] = TradeStatus.closed.value

        return trade


if __name__ == '__main__':
    pass
