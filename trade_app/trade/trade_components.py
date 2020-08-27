from enum import Enum


class TradeComponents(Enum):
    order_id = 0
    trade_id = 1
    time_stamp = 2
    year = 3
    month = 4
    day = 5
    hour = 6
    minute = 7
    ticker = 8
    buy_price = 9
    sell_price = 10
    quantity = 11
    cost = 12
    order_type = 13
    trader_id = 14
    profit = 15
    result = 16
    status = 17


class TradeResults(Enum):
    positive = 'P'
    negative = 'N'
    waiting = 'W'


class TradeStatus(Enum):
    working = True
    closed = False
