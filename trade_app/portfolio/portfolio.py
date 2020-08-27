from trade_app.orders import OrderComponents
from trade_app.trade import TradeComponents, TradeStatus, TradeResults
from trade_app.config.config_portfolio import ConfigPortfolio


class Portfolio:
    def __init__(self, config_obj, is_initial=False):

        if is_initial:
            self._capital = int(config_obj[ConfigPortfolio.initial_capital.name]) if int(
                config_obj[ConfigPortfolio.initial_capital.name]) >= 0 else 0.0

        else:
            self._capital = config_obj

    @property
    def capital(self):
        return self._capital

    @capital.setter
    def capital(self, value):
        if isinstance(value, float) and value >= 0:
            self._capital = value

    def increase_capital(self, value):
        if isinstance(value, float):
            self.capital += value

    def decrease_capital(self, value):
        if isinstance(value, float) and value >= 0:
            tmp_capital = self.capital
            tmp_capital -= value
            if tmp_capital < 0:
                print('No tiene suficiente capital para realaizar la operación')

            else:
                self.capital = tmp_capital


if __name__ == '__main__':
    pass
