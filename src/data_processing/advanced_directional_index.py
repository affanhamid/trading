import pandas as pd
import talib as ta
from .indicator import Indicator

class AverageDirectionalIndex(Indicator):
    """
    Class to calculate and evaluate the Average Directional Index (ADX) of a given dataset.

    Attributes:
        timeperiod (int): The time period over which to calculate the ADX. Default is 14.
    """
    def __init__(self, timeperiod: int = 14):
        """
        Initializes the AverageDirectionalIndex with a specified time period.

        Args:
            timeperiod (int): The time period over which to calculate the ADX. Default is 14.
        """
        self.timeperiod = timeperiod
        super().__init__()

    def calculate(self, data: pd.DataFrame) -> None:
        """
        Calculates the ADX for the given data and adds it as a new column to the DataFrame.

        Args:
            data (pd.DataFrame): The input data containing 'high', 'low', and 'price' columns.

        Returns:
            None
        """
        data = self.estimate_high_low(data)
        data['ADX'] = ta.ADX(data['high'], data['low'], data['price'], timeperiod=self.timeperiod)

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        """
        Evaluates the ADX value to determine the strength of the trend.

        Args:
            data (pd.DataFrame): The input data containing the 'ADX' column.

        Returns:
            str: A string indicating the strength of the trend ('strong_trend', 'weak_trend', or 'neutral').
        """
        if data['ADX'].iloc[-1] > 25:
            return 'strong_trend'
        elif data['ADX'].iloc[-1] < 20:
            return 'weak_trend'
        else:
            return 'neutral'
