from .strategy import Strategy
from pandas import DataFrame
from data_processing.indicator import Indicator

class PureIndicator(Strategy):
    """
    A trading strategy class that uses the Awesome Indicator to determine buy or sell signals.
    This class inherits from the Strategy base class and is designed to test the effectiveness
    of the Awesome Indicator in a trading strategy.
    """

    def __init__(self, indicator: Indicator):
        """
        Initialize the TestIndicator strategy with the Awesome Indicator.
        This sets up the strategy to use the Awesome Indicator for generating trading signals.
        """
        super().__init__([indicator])
        self.signals_to_graph = [['MACD', 'MACD_Signal']]
        
    def process_data(self, data: DataFrame, quantity: int):
        """
        Process the given data to execute trading orders based on signals from the Awesome Indicator.
        This method overrides the process_data method from the Strategy superclass to implement
        the specific logic for the Awesome Indicator.

        Args:
            data (DataFrame): The market data to be processed.
            quantity (int): The amount to buy or sell based on the trading signals.
        """
        super().process_data(data, quantity)
