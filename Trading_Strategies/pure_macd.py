from Data_Processing.MACD import MACD
from Order_Management.order_manager import OrderManager

class MACD_Strategy:
    def __init__(self):
        self.MACD = MACD()
        self.bought = False
        self.order_manager = OrderManager()
        
    def process_data(self, data, quantity):

        self.MACD.calculate_macd(data)

        if data.shape[0] > 2:
            order_type = self.MACD.evaluate_signal(data)

            if order_type == 'buy' and not self.bought:
                self.bought = True
                self.order_manager.buy(price=data.iloc[-1].price, time=data.iloc[-1].time.time(), quantity=quantity)
            elif order_type == 'sell' and self.bought:
                self.bought = False
                self.order_manager.sell(price=data.iloc[-1].price, time=data.iloc[-1].time.time(), quantity=quantity)