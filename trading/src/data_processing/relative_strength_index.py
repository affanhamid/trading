import pandas as pd
import talib as ta
from .indicator import Indicator

class RSI(Indicator):
    """
    Represents the Relative Strength Index (RSI) indicator which is a popular momentum oscillator used in technical analysis.
    """

    def __init__(self, time_period: int = 14):
        """
        Initializes the RSI indicator with a specified time period.

        Args:
            time_period (int): The number of periods to calculate the RSI. Default is 14.
        """
        self.time_period = time_period

    def calculate(self, data: pd.DataFrame) -> None:
        """
        Calculates the RSI values for the given data.

        Args:
            data (pd.DataFrame): A DataFrame containing the price data with a 'price' column.

        Modifies:
            data (pd.DataFrame): Adds an 'RSI' column with the calculated RSI values.
        """
        data['RSI'] = ta.RSI(data['price'], timeperiod=self.time_period)

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        """
        Evaluates the trading signal based on the RSI values.

        Args:
            data (pd.DataFrame): A DataFrame that contains at least one row and an 'RSI' column.

        Returns:
            str: A trading signal ('buy', 'sell', or 'hold') based on the RSI value of the last row.
                 'buy' if RSI < 30, 'sell' if RSI > 70, otherwise 'hold'.
        """
        last_row = data.iloc[-1]
        if last_row['RSI'] < 30:
            return 'buy'
        elif last_row['RSI'] > 70:
            return 'sell'
        else:
            return 'hold'
