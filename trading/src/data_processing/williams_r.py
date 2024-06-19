import pandas as pd
import talib as ta
from .indicator import Indicator


class WilliamsR(Indicator):
    def __init__(self, timeperiod: int = 14):
        self.timeperiod = timeperiod

    def calculate(self, data: pd.DataFrame) -> None:
        data = self.estimate_high_low(data)
        data['Williams_%R'] = ta.WILLR(data['high'], data['low'], data['price'], timeperiod=self.timeperiod)

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        last_row = data.iloc[-1]
        if last_row['Williams_%R'] > -20:
            return 'sell'
        elif last_row['Williams_%R'] < -80:
            return 'buy'
        else:
            return 'hold'
