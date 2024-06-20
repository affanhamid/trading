from __future__ import annotations
from utility.logger import log_buy_order, log_sell_order, calculate_brokerage_fee

class OrderManager:
    """Manages buy and sell orders for trading."""

    def __init__(self):
        """Initializes the OrderManager with no data."""
        self.data = None

    def set_data(self, data: dict) -> None:
        """
        Sets the data for the OrderManager.

        Args:
            data (dict): The data to be managed.
        """
        self. data = data

    @log_buy_order
    def buy(self, price: float, time: str, quantity: int, strategy: 'Strategy', interval: int) -> None:
        """
        Executes a buy order and logs the transaction.

        Args:
            price (float): The price at which to buy.
            time (str): The timestamp of the order.
            quantity (int): The amount to buy.
        """
        pass

    @log_sell_order
    @calculate_brokerage_fee
    def sell(self, price: float, time: str, quantity: int, strategy: 'Strategy', interval: int) -> None:
        """
        Executes a sell order, calculates brokerage, and logs the transaction.

        Args:
            price (float): The price at which to sell.
            time (str): The timestamp of the order.
            quantity (int): The amount to sell.
        """
        pass