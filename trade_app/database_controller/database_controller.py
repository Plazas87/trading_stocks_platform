import psycopg2 as db
from datetime import datetime

from trade_app.orders import OrderComponents
from trade_app.trade import TradeComponents
from trade_app.config import DataBaseConnection


class DatabaseController:
    """Class that controls database connections"""

    def __init__(self, db_config_obj):
        self.connection_status = False
        self._user = db_config_obj[DataBaseConnection.user.name]
        self._password = db_config_obj[DataBaseConnection.password.name]
        self._address = db_config_obj[DataBaseConnection.address.name]
        self._port = db_config_obj[DataBaseConnection.port.name]
        self._database = db_config_obj[DataBaseConnection.database.name]

    def __new__(cls, name=None, params=None):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DatabaseController, cls).__new__(cls)
        return cls.instance

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        if isinstance(value, str):
            self._user = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if isinstance(value, str):
            self._address = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        if isinstance(value, int):
            self._port = value

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, value):
        if isinstance(value, str):
            self._database = value

    def _connect(self):
        """Establishes a connection with the database"""
        try:
            # conn = None
            conn = db.connect(user=self.user,
                              password=self._password,
                              host=self.address,
                              port=self.port,
                              database=self.database)

            self.connection_status = True
            return conn
        except Exception as e:
            print(f'Error while connecting to the database: {e}')
            return None

    def _close_connection(self, connection):
        """Close the connection with the database"""
        try:
            connection.close()
            self.connection_status = False

        except Exception as e:
            print(f'Unable to close the database connection: {e}')
            return None

    def save_order(self, order, info=None):
        """Save the orders into database"""
        # connect with database
        conn = self._connect()

        query = "INSERT INTO orders VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        if conn is not None:
            cursor = conn.cursor()
            try:
                data = tuple(order.values())
                cursor.execute(query, data)

            except Exception as e:
                print(f'Error while saving the order: {e}')
                cursor.close()
                self._close_connection(conn)
                return False
            else:
                conn.commit()
                cursor.close()
                self._close_connection(conn)
                return True

    def save_capital(self, capital, info=None):
        """Set initial or current capital for a session"""
        conn = self._connect()

        query = "INSERT INTO capital (timestamp, capital) VALUES (%s, %s)"

        if conn is not None:
            cursor = conn.cursor()
            try:
                data = (datetime.now(), capital)
                cursor.execute(query, data)

            except Exception as e:
                print(f'Error while updating capital: {e}')
                cursor.close()
                self._close_connection(conn)
                return False
            else:
                conn.commit()
                cursor.close()
                self._close_connection(conn)
                return True

    def get_capital(self):
        """Get the current capital available to trade"""
        conn = self._connect()

        query = "SELECT capital FROM capital ORDER BY timestamp DESC LIMIT 1"

        if conn is not None:
            cursor = conn.cursor()
            try:
                cursor.execute(query)

            except Exception as e:
                print(f'Error while getting available capital to trade: {e}')
                cursor.close()
                self._close_connection(conn)

            else:
                data_query = cursor.fetchall()[0][0]
                cursor.close()
                self._close_connection(conn)
                return data_query

    def validate_initial_capital(self):
        """Check if capital has been initialized"""
        conn = self._connect()

        query = "SELECT count(capital) FROM capital"

        if conn is not None:
            cursor = conn.cursor()
            try:
                cursor.execute(query)
                data_query = cursor.fetchall()[0][0]

            except Exception as e:
                cursor.close()
                self._close_connection(conn)

            else:
                cursor.close()
                self._close_connection(conn)
                return data_query

    def open_trade(self, trade_dict):
        """Save a new trade into de database"""
        conn = self._connect()

        query = "INSERT INTO openorders VALUES" \
                " (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        if conn is not None:
            cursor = conn.cursor()
            try:
                data = tuple(trade_dict.values())
                cursor.execute(query, data)

            except Exception as e:
                print(f'Error while opening a trade: {e}')
                cursor.close()
                self._close_connection(conn)
                return False
            else:
                conn.commit()
                cursor.close()
                self._close_connection(conn)
                return True

    def get_open_trades(self, ticker):
        """This method is in charge of putting in memory the open trades so that the user can
        sees them on the screen every time he closes an order"""
        # connect with database
        conn = self._connect()

        if ticker is None:
            query = "SELECT order_id, ticker, buy_price, quantity " \
                    "FROM openorders " \
                    "WHERE status = true " \
                    "ORDER BY time_stamp DESC"

        else:
            query = "SELECT order_id, ticker, buy_price, quantity " \
                    "FROM openorders " \
                    "WHERE ticker = (%s) AND status = true " \
                    "ORDER BY time_stamp DESC"

        if conn is not None:
            cursor = conn.cursor()
            try:
                data = (ticker,)
                cursor.execute(query, data)
                data_query = cursor.fetchall()

            except Exception as e:
                print(f'Error while reading open trades: {e}')
                cursor.close()
                self._close_connection(conn)

            else:
                open_trades = []
                for trade in data_query:
                    tmp = {TradeComponents.order_id.name: trade[0],
                           TradeComponents.ticker.name: trade[1],
                           TradeComponents.quantity.name: trade[2],
                           TradeComponents.cost.name: trade[3]}

                    open_trades.append(tmp)

                cursor.close()
                self._close_connection(conn)
                return open_trades

    def get_order_by_id(self, id):
        """Get an open order by id"""
        conn = self._connect()

        query = "SELECT ticker, quantity, trade_id FROM openorders WHERE order_id = (%s)"
        data = (id,)

        if conn is not None:
            cursor = conn.cursor()
            try:
                cursor.execute(query, data)
                data_query = cursor.fetchall()[0]

            except Exception as e:

                print(f'There are no open trades with the given id: {e}')
                cursor.close()
                self._close_connection(conn)
                return False, []

            else:
                cursor.close()
                self._close_connection(conn)
                return True, data_query

    def get_trade_by_id(self, id):
        """Get an open trade by ID"""
        conn = self._connect()

        query = "SELECT cost, sell_price, quantity FROM openorders WHERE trade_id = (%s) " \
                "AND status = true"
        data = (id,)

        if conn is not None:
            cursor = conn.cursor()
            try:
                cursor.execute(query, data)
                data_query = cursor.fetchall()[0]

            except Exception as e:
                print(f'There are no trades with the given ID: {e}')
                cursor.close()
                self._close_connection(conn)
                return False, {}

            else:
                data_query = {OrderComponents.cost.name: data_query[0],
                              OrderComponents.sell_price.name: data_query[1],
                              OrderComponents.quantity.name: data_query[2]}

                cursor.close()
                self._close_connection(conn)
                return True, data_query

    def update_trade_by_id(self, trade_to_update, trade_id):
        """Update the trade status after a close order execution"""
        conn = self._connect()

        query = "UPDATE openorders SET sell_price = %s, profit = %s, result = %s, status = %s " \
                "WHERE trade_id = %s;"

        data = (trade_to_update[OrderComponents.sell_price.name],
                trade_to_update[TradeComponents.profit.name],
                trade_to_update[TradeComponents.result.name],
                trade_to_update[TradeComponents.status.name],
                trade_id)

        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute(query, data)

            except Exception as e:
                print(f'Error while updating or closing the trade: {e}')
                cursor.close()
                self._close_connection(conn)
                return False

            else:
                conn.commit()
                cursor.close()
                self._close_connection(conn)

                return True


if __name__ == '__main__':
    query = DatabaseController('postgresql')
    var = query.selectQuery('users', '*', filter_table='acpr87@gmail.com')
    if var:
        print(type(var))
        print('True')
    else:
        print(False)
    print(var)
    print(query)
