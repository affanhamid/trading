import pandas as pd
import talib as ta
from .indicator import Indicator

class AverageTrueRange(Indicator):
    """
    A class to calculate the Average True Range (ATR) of stock prices, which is a technical analysis indicator
    used to measure market volatility.

    Attributes:
        timeperiod (int): The number of periods to use when calculating the ATR.
    """

    def __init__(self, timeperiod: int = 14):
        """
        Initializes the AverageTrueRange with a specified time period.

        Args:
            timeperiod (int): The number of periods over which the ATR should be calculated. Default is 14.
        """
        self.timeperiod = timeperiod

    def calculate(self, data: pd.DataFrame) -> None:
        """
        Calculates the Average True Range (ATR) and adds it as a new column to the DataFrame.

        Args:
            data (pd.DataFrame): The input data containing the columns 'high', 'low', and 'price'.

        Returns:
            None: The function adds an 'ATR' column to the input DataFrame.
        """
        data = self.estimate_high_low(data)
        data['ATR'] = ta.ATR(data['high'], data['low'], data['price'], timeperiod=self.timeperiod)

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        """
        Evaluates the trading signal based on the ATR values.

        Args:
            data (pd.DataFrame): The DataFrame with the 'ATR' column.

        Returns:
            str: A signal string which can be 'buy', 'sell', or 'hold' based on the ATR trend.
        """
        if data['ATR'].iloc[-1] > data['ATR'].iloc[-2]:
            return 'buy'
        elif data['ATR'].iloc[-1] < data['ATR'].iloc[-2]:
            return 'sell'
        else:
            return 'hold'