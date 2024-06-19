import pandas as pd
import talib as ta
from .indicator import Indicator

class KeltnerChannel(Indicator):
    """
    Keltner Channel is a volatility-based technical indicator that combines an exponential moving average
    of the closing price with two bands that are spaced above and below the EMA by a multiple of the Average True Range (ATR).

    Attributes:
        time_period1 (int): Time period for the Exponential Moving Average (EMA).
        time_period2 (int): Time period for the Average True Range (ATR).
        nbdevup (int): Number of ATRs to add to the EMA for the upper band.
        nbdevdn (int): Number of ATRs to subtract from the EMA for the lower band.
    """

    def __init__(self, time_period1: int = 20, time_period2: int = 10, nbdevup: int = 2, nbdevdn: int = 2):
        """
        Initializes the KeltnerChannel with specified parameters.

        Args:
            time_period1 (int): Time period for the EMA calculation.
            time_period2 (int): Time period for the ATR calculation.
            nbdevup (int): Multiplier for the upper band calculation.
            nbdevdn (int): Multiplier for the lower band calculation.
        """
        self.time_period1 = time_period1
        self.time_period2 = time_period2
        self.nbdevup = nbdevup
        self.nbdevdn = nbdevdn

    def calculate(self, data: pd.DataFrame) -> None:
        """
        Calculates the Keltner Channel and updates the DataFrame with the 'keltner_upper', 'keltner_middle', and 'keltner_lower' columns.

        Args:
            data (pd.DataFrame): DataFrame containing the 'price', 'high', and 'low' columns.

        Returns:
            None: The function modifies the DataFrame in place, adding three new columns.
        """
        data = self.estimate_high_low(data)
        ema_close = ta.EMA(data['price'], timeperiod=self.time_period1)
        atr = ta.ATR(data['high'], data['low'], data['price'], timeperiod=self.time_period2)

        data['keltner_upper'] = ema_close + self.nbdevup * atr
        data['keltner_middle'] = ema_close
        data['keltner_lower'] = ema_close - self.nbdevdn * atr

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        """
        Evaluates the trading signal based on the last row of the DataFrame.

        Args:
            data (pd.DataFrame): DataFrame containing the 'price', 'keltner_upper', and 'keltner_lower' columns.

        Returns:
            str: Returns 'buy' if the price is above the upper band, 'sell' if below the lower band, and 'hold' otherwise.
        """
        last_row = data.iloc[-1]
        if last_row['price'] > last_row['keltner_upper']:
            return 'buy'
        elif last_row['price'] < last_row['keltner_lower']:
            return 'sell'
        else:
            return 'hold'
