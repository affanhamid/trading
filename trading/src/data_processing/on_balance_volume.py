import pandas as pd
import talib as ta
from .indicator import Indicator

class OnBalanceVolume(Indicator):
    """
    This class is designed to calculate the On-Balance Volume (OBV) for a given dataset.
    OBV is a technical trading momentum indicator that uses volume flow to predict changes in stock price.
    """

    def calculate_obv(self, data: pd.DataFrame) -> None:
        """
        Calculate the On-Balance Volume (OBV) and append it as a new column to the DataFrame.

        Parameters:
        data (pd.DataFrame): A DataFrame containing at least 'close' and 'volume' columns.

        Returns:
        None: The function adds an 'OBV' column to the DataFrame in-place.
        """
        data['OBV'] = ta.OBV(data['close'], data['volume'])