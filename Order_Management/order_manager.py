from Utility.logger import log_buy_order, log_sell_order
from Utility.utils import calculate_brokerage_fee

class OrderManager:

    def __init__(self):
        self.data = None

    def set_data(self, data):
        self.data = data

    @log_buy_order
    def buy(self, price, time, quantity):
        # print(f'{time} Buying @ {price}')
        pass

    @log_sell_order
    @calculate_brokerage_fee
    def sell(self, price, time, quantity):
        # print(f'{time} Selling @ {price}')
        pass
