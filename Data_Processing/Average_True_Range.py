import pandas as pd
import talib as ta
from .Indicator import Indicator

class AverageTrueRange(Indicator):
    def __init__(self, timeperiod: int = 14):
        self.timeperiod = timeperiod

    def calculate(self, data: pd.DataFrame) -> None:
        data = self.estimate_high_low(data)
        data['ATR'] = ta.ATR(data['high'], data['low'], data['price'], timeperiod=self.timeperiod)

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        if data['ATR'].iloc[-1] > data['ATR'].iloc[-2]:
            return 'buy'
        elif data['ATR'].iloc[-1] < data['ATR'].iloc[-2]:
            return 'sell'
        else:
            return 'hold'