from order_management.order_manager import OrderManager
from data_processing.indicator import Indicator
import pandas as pd

class Strategy:
    def __init__(self, indicators: list[type[Indicator]]):
        """
        Initializes the Strategy class with a list of indicator classes.

        Args:
            indicators (list[type[Indicator]]): A list of classes derived from the Indicator base class.
        """
        self.bought = False  # Flag to track if a buy order has been executed
        self.order_manager = OrderManager()  # Manages trading orders
        self.indicators = [indicator() for indicator in indicators]  # Instantiate indicators

    def process_data(self, data: pd.DataFrame, quantity: int):
        """
        Analyzes the provided market data using the specified indicators and executes trading orders.

        This method calculates the indicators for the given data and then checks if the conditions
        for placing a buy or sell order are met based on the first indicator's signal.

        Args:
            data (pd.DataFrame): The market data on which the indicators will operate.
            quantity (int): The amount to buy or sell.
        """
        for indicator in self.indicators:
            indicator.calculate(data)

        if data.shape[0] > 2:
            signals = [indicator.evaluate_signal(data) for indicator in self.indicators]
            self.add_order(signals[0], data, quantity)

    def add_order(self, order_type: str, data: pd.DataFrame, quantity: int):
        """
        Places a buy or sell order based on the provided order type if the conditions are met.

        This method checks the current state of the 'bought' flag and the order type to decide
        whether to place a buy or sell order. It then calls the appropriate method from the
        OrderManager to execute the order.

        Args:
            order_type (str): The type of order to place ('buy' or 'sell').
            data (pd.DataFrame): The market data used to determine the price and time of the order.
            quantity (int): The amount to buy or sell.
        """
        if order_type == 'buy' and not self.bought:
            self.bought = True
            self.order_manager.buy(price=data.iloc[-1].price, time=data.iloc[-1].time.time(), quantity=quantity)

        elif order_type == 'sell' and self.bought:
            self.bought = False
            self.order_manager.sell(price=data.iloc[-1].price, time=data.iloc[-1].time.time(), quantity=quantity)