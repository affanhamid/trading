import pandas as pd
import talib as ta
from .Indicator import Indicator

class IchimokuCloud(Indicator):
    def __init__(self, timeperiod1: int = 9, timeperiod2: int = 26, timeperiod3: int = 52):
        self.timeperiod1 = timeperiod1
        self.timeperiod2 = timeperiod2
        self.timeperiod3 = timeperiod3

    def calculate(self, data: pd.DataFrame) -> None:
        data = self.estimate_high_low(data)
        high = data['high']
        low = data['low']
        close = data['price']

        # Tenkan-sen (Conversion Line): (timeperiod1-period high + timeperiod1-period low)/2
        data['Tenkan Sen'] = (high.rolling(window=self.timeperiod1).max() + low.rolling(window=self.timeperiod1).min()) / 2

        # Kijun-sen (Base Line): (timeperiod2-period high + timeperiod2-period low)/2
        data['Kijun Sen'] = (high.rolling(window=self.timeperiod2).max() + low.rolling(window=self.timeperiod2).min()) / 2

        # Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2, shifted timeperiod2 periods ahead
        data['Senkou Span A'] = ((data['Tenkan Sen'] + data['Kijun Sen']) / 2).shift(self.timeperiod2)

        # Senkou Span B (Leading Span B): (timeperiod3-period high + timeperiod3-period low)/2, shifted timeperiod2 periods ahead
        data['Senkou Span B'] = ((high.rolling(window=self.timeperiod3).max() + low.rolling(window=self.timeperiod3).min()) / 2).shift(self.timeperiod2)

        # Chikou Span (Lagging Span): Close plotted timeperiod2 days in the past
        data['Chikou Span'] = close.shift(self.timeperiod2)

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        """
        Evaluates the trading signal based on the Ichimoku Cloud.

        Args:
            data (pd.DataFrame): DataFrame containing Ichimoku Cloud data.

        Returns:
            str: 'buy', 'sell', or 'hold' based on the Ichimoku Cloud strategy.
        """
        last_row = data.iloc[-1]

        if last_row['price'] > last_row['Senkou Span A'] and last_row['price'] > last_row['Senkou Span B']:
            return 'buy'
        elif last_row['price'] < last_row['Senkou Span A'] and last_row['price'] < last_row['Senkou Span B']:
            return 'sell'
        else:
            return 'hold'