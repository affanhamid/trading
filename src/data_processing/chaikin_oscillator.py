import pandas as pd
import talib as ta
from .indicator import Indicator

class ChaikinOscillator(Indicator):
    """
    Chaikin Oscillator class derived from Indicator base class, used to compute the Chaikin Oscillator
    for a given stock data. The Chaikin Oscillator is an indicator that measures momentum of the 
    Accumulation Distribution Line using the MACD formula.

    Attributes:
        fastperiod (int): The short period for the exponential moving average (EMA). Default is 3.
        slowperiod (int): The long period for the exponential moving average (EMA). Default is 10.
    """

    def __init__(self, fastperiod: int = 3, slowperiod: int = 10):
        """
        Initializes the Chaikin Oscillator with specified periods for the fast and slow EMAs.

        Args:
            fastperiod (int): The short period for the exponential moving average (EMA). Default is 3.
            slowperiod (int): The long period for the exponential moving average (EMA). Default is 10.
        """
        self.fastperiod = fastperiod
        self.slowperiod = slowperiod

    def calculate_chaikin(self, data: pd.DataFrame) -> None:
        """
        Calculates the Chaikin Oscillator values for the given DataFrame and adds it as a new column 'Chaikin'.

        This method first estimates the high and low prices using the estimate_high_low method and then
        computes the Chaikin Oscillator using the TA-Lib's ADOSC function.

        Args:
            data (pd.DataFrame): The stock market data containing 'high', 'low', 'close', and 'volume' columns.

        Returns:
            None: The function adds a new column 'Chaikin' to the DataFrame in-place.
        """
        data = self.estimate_high_low(data)
        data['Chaikin'] = ta.ADOSC(data['high'], data['low'], data['close'], data['volume'], fastperiod=self.fastperiod, slowperiod=self.slowperiod)