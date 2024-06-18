from Order_Management.order_manager import OrderManager
import pandas as pd
from Data_Processing.Indicator import Indicator

class Strategy:
    def __init__(self, indicators: list[type[Indicator]]):
        self.bought = False  # Flag to track if a buy order has been executed
        self.order_manager = OrderManager()  # Manages trading orders
        self.indicators = [indicator() for indicator in indicators]
    

    def process_data(self, data: pd.DataFrame, quantity: int):
        """
        Process the given data to execute trading orders based on MACD signals.

        Args:
            data (DataFrame): The market data.
            quantity (int): The amount to buy or sell.
        """
        for indicator in self.indicators:
            indicator.calculate(data)

        if data.shape[0] > 2:
            signals = [indicator.evaluate_signal(data) for indicator in self.indicators]
            self.add_order(signals[0], data, quantity)

    def add_order(self, order_type: str, data: pd.DataFrame, quantity: int):
        if order_type == 'buy' and not self.bought:
            self.bought = True
            self.order_manager.buy(price=data.iloc[-1].price, time=data.iloc[-1].time.time(), quantity=quantity)

        elif order_type == 'sell' and self.bought:
            self.bought = False
            self.order_manager.sell(price=data.iloc[-1].price, time=data.iloc[-1].time.time(), quantity=quantity)