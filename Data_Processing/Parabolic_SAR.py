import pandas as pd
import talib as ta
from .Indicator import Indicator

class ParabolicSAR(Indicator):
    def __init__(self, acceleration: float = 0.02, maximum: float = 0.2):
        self.acceleration = acceleration
        self.maximum = maximum

    def calculate(self, data: pd.DataFrame) -> None:
        data = self.estimate_high_low(data)
        data['SAR'] = ta.SAR(data['high'], data['low'], acceleration=self.acceleration, maximum=self.maximum)

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        last_row = data.iloc[-1]
        second_last_row = data.iloc[-2]
        if second_last_row['price'] > second_last_row['SAR'] and last_row['price'] < last_row['SAR']:
            return 'sell'
        elif second_last_row['price'] < second_last_row['SAR'] and last_row['price'] > last_row['SAR']:
            return 'buy'
        else:
            return 'hold'