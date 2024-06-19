import pandas as pd
import talib as ta
from .indicator import Indicator

class IchimokuCloud(Indicator):
    """
    Represents the Ichimoku Cloud indicator, which is used to gauge momentum along with future areas of support and resistance.

    Attributes:
        timeperiod1 (int): The number of periods used to calculate the Tenkan-sen (Conversion Line).
        timeperiod2 (int): The number of periods used to calculate the Kijun-sen (Base Line) and to shift the Chikou Span and Senkou Spans.
        timeperiod3 (int): The number of periods used to calculate the Senkou Span B (Leading Span B).
    """
    def __init__(self, timeperiod1: int = 9, timeperiod2: int = 26, timeperiod3: int = 52):
        self.timeperiod1 = timeperiod1
        self.timeperiod2 = timeperiod2
        self.timeperiod3 = timeperiod3

    def calculate(self, data: pd.DataFrame) -> None:
        """
        Calculates the Ichimoku Cloud indicator values.

        Args:
            data (pd.DataFrame): The market data on which the Ichimoku Cloud will be calculated.

        Modifies:
            data (pd.DataFrame): Adds the Ichimoku Cloud indicator components as new columns.
        """
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
        elif last_row['price'] < last_row['Senkou Span A'] and last_row['price'] < last
            return 'sell'
        else:
            return 'hold'