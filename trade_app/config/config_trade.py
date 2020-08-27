from enum import Enum


class ConfigTrade(Enum):
    max_lost_per_trade = 0
    max_lost_per_day = 1
    max_buy_per_trade = 2
