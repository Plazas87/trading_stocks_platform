from .builconfigurations import BuildConfiguration
from .app_CLI import Controller
from .orders import BuyOrder, SellOrder
from random import randint


if __name__ == '__main__':
    configuration_obj = BuildConfiguration()
    controller = Controller(configuration_obj.config_obj)
    controller.run()

    stocks = ['NFLX', 'SPY']

    while controller.status:
        print()
        interface = input(
            'Chose and option: 1 to buy, 2 to sell y 0 to exit \nType your chose: ')
        if interface == '1':
            try:
                buy_order = BuyOrder(stocks[0], buy_price=randint(1, 40), quantity=randint(1, 10))
                print(f'Order cost: {buy_order.buy_price * buy_order.quantity}')
                status, order_dict = controller.open_position(buy_order)
                if status:
                    # show information after the order execution
                    print('Trade successfully executed.')
                    print('An order with the following characteristics has been executed:')
                    for key in order_dict.keys():
                        print(' - ' + key + ': ', end='')
                        print(str(order_dict[key]))
                    print('\n')

            except Exception as e:
                print(e, ' - The action could not be executed - ', e.args)

        elif interface == '2':
            print()
            print('    Connecting to database...')
            print()
            open_trades, active_trades_list = controller.get_open_trades_ticker()
            if open_trades:
                print()
                print('Open trades:')
                for key, trade_dict in enumerate(active_trades_list):
                    print(f' - {str(key)}: ', end='')
                    for trade_key, trade_value in trade_dict.items():
                        print(f'|{trade_key}: {trade_value}| ', end='')

                    print()

                trade_id = int(input('Digite el ID de la orden que desea cerrar: '))
                status, trade_to_close = controller.get_open_trades_id(trade_id)

                if status:
                    sell_order = SellOrder(trade_to_close[0], sell_price=randint(20, 100), quantity=trade_to_close[1])
                    order_status, order_dict, profit = controller.close_position(sell_order, trade_to_close[2])
                    if order_status:
                        # show information after the order execution
                        print('Trade successfully executed.')
                        print()
                        print(f'Profit: {profit}')
                        print('An order with the following characteristics has been executed:')
                        for key in order_dict.keys():
                            print(' - ' + key + ': ', end='')
                            print(str(order_dict[key]))
                    print()

                else:
                    print('Wrong ID')
