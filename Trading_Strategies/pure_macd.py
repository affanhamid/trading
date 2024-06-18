from Data_Processing.MACD import MACD
from .Strategy import Strategy
from pandas import DataFrame

class MACD_Strategy(Strategy):
    """A trading strategy class that uses MACD to determine buy or sell signals."""

    def __init__(self):
        """Initialize the MACD strategy with a MACD processor."""
        super().__init__(MACD)  # Initialize the base Strategy class with MACD as the indicator
        
    def process_data(self, data: DataFrame, quantity: int):
        """
        Process the given data to execute trading orders based on MACD signals using the superclass's method.

        Args:
            data (DataFrame): The market data.
            quantity (int): The amount to buy or sell.
        """
        super().process_data(data, quantity)  # Use the process_data method from the Strategy superclass
