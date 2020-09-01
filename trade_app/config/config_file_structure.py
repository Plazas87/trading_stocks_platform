from enum import Enum


class ConfigFileSection(Enum):
    postgresql = 0
    portfolio = 1
    trader = 2
    consumer = 3
