from enum import Enum


class StockTable(Enum):
    date = 0
    open_price = 1
    high = 2
    low = 3
    close_price = 4
    adj_close = 5
    volume = 6
