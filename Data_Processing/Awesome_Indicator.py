import pandas as pd
import talib as ta
from .Indicator import Indicator

class AwesomeIndicator(Indicator):
    def __init__(self, short_period: int = 5, long_period: int = 34):
        self.short_period = short_period
        self.long_period = long_period

    def calculate(self, data: pd.DataFrame) -> None:
        self.estimate_high_low(data)
        median_price = (data['high'] + data['low']) / 2
        data['AO'] = median_price.rolling(window=self.short_period).mean() - median_price.rolling(window=self.long_period).mean()

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        last_row = data.iloc[-1]
        if abs(last_row['AO']) > 10:
            return 'strong signal'
        else:
            return 'weak signal'
