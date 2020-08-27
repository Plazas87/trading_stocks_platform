class CreateOrderException(Exception):
    def __init__(self, message='CreateOrderException'):
        Exception.__init__(self, message)


class CloseOrderException(Exception):
    def __init__(self, message='CreateOrderException'):
        Exception.__init__(self, message)


class QueryException(Exception):
    def __init__(self, table, message='QueryException'):
        Exception.__init__(self, message)


class MaxBuyPerTradeException(Exception):
    def __init__(self, message='MaxBuyPerTradeException'):
        Exception.__init__(self, message)

