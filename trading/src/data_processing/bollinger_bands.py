import pandas as pd
import talib as ta
from .indicator import Indicator

class BollingerBands(Indicator):
    def __init__(self, window_size: int = 20, num_std_dev: float = 2):
        """
        Initializes the Bollinger Bands class with given window size and number of standard deviations.

        Args:
            window_size (int): The size of the moving window.
            num_std_dev (float): The number of standard deviations to use for the upper and lower bands.
        """
        self.window_size = window_size
        self.num_std_dev = num_std_dev

    def calculate(self, data: pd.DataFrame) -> None:
        """
        Calculates the Bollinger Bands for the given data.

        Args:
            data (pd.DataFrame): DataFrame containing price data.
        """
        data['upper_band'], data['middle_band'], data['lower_band'] = ta.BBANDS(data['price'], timeperiod=self.window_size, nbdevup=self.num_std_dev, nbdevdn=self.num_std_dev, matype=0)


    def evaluate_signal(self, data: pd.DataFrame) -> str:
        """
        Evaluates the trading signal based on the Bollinger Bands.

        Args:
            data (pd.DataFrame): DataFrame containing Bollinger Bands data.

        Returns:
            str: 'buy', 'sell', or 'hold' based on the Bollinger Bands strategy.
        """
        # Get the last two rows of data
        last_row = data.iloc[-1]
        second_last_row = data.iloc[-2]

        # Determine the trading signal
        if (second_last_row['price'] > second_last_row['upper_band'] and last_row['price'] < last_row['upper_band']):
            return 'sell'
        elif (second_last_row['price'] < second_last_row['lower_band'] and last_row['price'] > last_row['lower_band']):
            return 'buy'
        else:
            return 'hold'
