import pandas as pd
from .Indicator import Indicator

class RelativeVigorIndex(Indicator):
    def __init__(self, time_period: int = 10):
        self.time_period = time_period

    def calculate(self, data: pd.DataFrame) -> None:
        self.estimate_high_low(data)
        data['open'] = data['price'].shift(1)
        num = ((data['price'] - data['open']) + 2 * (data['price'].shift(1) - data['open'].shift(1)) +
           2 * (data['price'].shift(2) - data['open'].shift(2)) + (data['price'].shift(3) - data['open'].shift(3))) / 6
        den = ((data['high'] - data['low']) + 2 * (data['high'].shift(1) - data['low'].shift(1)) +
           2 * (data['high'].shift(2) - data['low'].shift(2)) + (data['high'].shift(3) - data['low'].shift(3))) / 6

        # Calculate RVGI
        data['RVI'] = num.rolling(window=self.time_period).mean() / den.rolling(window=self.time_period).mean()
        data['RVI_Signal'] = data['RVI'].rolling(window=self.time_period).mean()

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        last_row = data.iloc[-1]
        if last_row['RVI'] > last_row['RVI_Signal']:
            return 'buy'
        elif last_row['RVI'] < last_row['RVI_Signal']:
            return 'sell'
        else:
            return 'hold'
