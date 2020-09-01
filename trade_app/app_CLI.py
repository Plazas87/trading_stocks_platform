from .portfolio import Portfolio
from .trader import Trader
from .orders import OrderComponents, OrderTypes
from .trade import TradeComponents
from .database_controller import DatabaseController
from .config import ConfigFileSection
from .consumer import Consumer


class Controller:
    def __init__(self, config_obj):
        # Database controller
        self._dbController = DatabaseController(config_obj[ConfigFileSection.postgresql.name])

        # Portfolio management
        if self.validate_initial_capital():
            self.portfolio = Portfolio(config_obj[ConfigFileSection.portfolio.name], is_initial=True)
            self._set_capital(self.portfolio.capital)

        else:
            self.portfolio = Portfolio(self.get_capital())

        # Trader for this session
        self.trader = Trader(config_obj[ConfigFileSection.trader.name])

        # Kafka data consumer
        self.consumer = Consumer(config_obj[ConfigFileSection.consumer.name])

        self.status = False
        print('Your trader ID para esta sesión is:', self.trader.id_trader)

    def run(self):
        self.status = True

    def open_position(self, buy_order):
        try:
            trade_status, trade_dict, order_dict = self.trader.prepare_trade(buy_order)

            if trade_status:
                if self.validate_buying_power(order_dict):
                    print(f'    Capital before execute the order (USD): {self.portfolio.capital}')
                    print()

                    if self.trader.execute_order(order_dict):
                        self.update_capital(order_dict)

                        if self._dbController.open_trade(trade_dict):
                            self._dbController.save_order(order_dict)

                            print(f'    Available capital for trade (USD): {self.portfolio.capital}')

                            return True, order_dict

                else:
                    print('Not enough capital to trade')
                    print(f'    Available capital for trade (USD): {self.portfolio.capital}')

                    return False, []
            else:
                print(f'The trade is not valid - STATUS: {trade_status}')
                return False, []

        except Exception as e:
            print(e)
            return False, []

    def close_position(self, sell_order, trade_id):
        try:
            # order_ready, order_dict = self.trader.prepare_order(sell_order)
            orders_status, trade_dict, order_dict = self.trader.prepare_trade(sell_order, trade_id=trade_id)
            if orders_status:

                print(f'Capital before execute the close order: {self.portfolio.capital}')
                if self.trader.execute_order(order_dict):
                    self._dbController.save_order(order_dict)

                    status, trade_to_update = self._dbController.get_trade_by_id(trade_id)
                    if status:

                        trade_to_update = self.trader.update_sell_price(trade_to_update,
                                                                        sell_order.sell_price)

                        trade_to_update = self.trader.update_profit(trade_to_update,
                                                                    sell_order.cost)

                        trade_to_update = self.trader.update_quantity(trade_to_update,
                                                                      sell_order.quantity)

                        trade_to_update = self.trader.update_result(trade_to_update)
                        trade_to_update = self.trader.update_status(trade_to_update)

                        self.update_capital(order_dict)
                        self._dbController.update_trade_by_id(trade_to_update, trade_id)

                        print('Trade successfully executed.')
                        print(f'Capital after execute the close order: {self.portfolio.capital}')

                    return True, order_dict, trade_to_update[TradeComponents.profit.name]
            else:
                print(f'The trade is not valid - STATUS: {orders_status}')
                return False, []

        except Exception as e:
            print(e)
            return False, []

    def validate_buying_power(self, order):
        cost = order[OrderComponents.buy_price.name] * order[OrderComponents.quantity.name]
        if cost > 0.0:
            max_buy_per_trade = (self.trader.max_buy_per_trade * self.portfolio.capital)
            if cost <= max_buy_per_trade:
                return True

            else:
                return False
        else:
            return False

    def get_open_trades_ticker(self, ticker=None):
        trade_list = self._dbController.get_open_trades(ticker=ticker)
        if len(trade_list) == 0:
            return False, trade_list

        else:
            return True, trade_list

    def validate_initial_capital(self):
        is_initial = self._dbController.validate_initial_capital()

        if is_initial:
            return False
        else:
            return True

    def update_capital(self, order, sell=None):
        if order[OrderComponents.order_type.name] == OrderTypes.buy.name:
            self.portfolio.decrease_capital(order[OrderComponents.cost.name])
            self._set_capital(self.portfolio.capital)

        elif order[OrderComponents.order_type.name] == OrderTypes.sell.name:
            value = order[OrderComponents.cost.name]
            self.portfolio.increase_capital(value)
            self._set_capital(self.portfolio.capital)

    def _set_capital(self, capital):
        return self._dbController.save_capital(capital)

    def get_capital(self):
        capital = self._dbController.get_capital()
        return capital

    def get_active_trades(self):
        self.get_open_trades_ticker()

    def get_open_trades_id(self, trade_id):
        status, trade = self._dbController.get_order_by_id(trade_id)
        if status:
            return status, trade

        else:
            return status, trade


if __name__ == '__main__':
    pass
