import pandas as pd
import talib as ta
from .Indicator import Indicator

class PivotPoints(Indicator):
    def __init__(self, timeperiod: int = 1):
        self.timeperiod = timeperiod

    def calculate(self, data: pd.DataFrame) -> None:
        data = self.estimate_high_low(data)
        data['pivot'] = (data['high'] + data['low'] + data['price']) / 3
        data['resistance1'] = 2 * data['pivot'] - data['low']
        data['support1'] = 2 * data['pivot'] - data['high']

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        last_row = data.iloc[-1]
        if last_row['price'] > last_row['resistance1']:
            return 'buy'
        elif last_row['price'] < last_row['support1']:
            return 'sell'
        else:
            return 'hold'