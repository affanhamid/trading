import pandas as pd
import talib as ta
from .Indicator import Indicator

# DONT HAVE VOLUMNE INFO

class AccumulationDistributionLine(Indicator):
    def calculate(self, data: pd.DataFrame) -> None:
        data = self.estimate_high_low(data)
        data['ADL'] = ta.AD(data['high'], data['low'], data['price'], data['volume'])

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        if data['ADL'].iloc[-1] > data['ADL'].iloc[-2]:
            return 'buy'
        elif data['ADL'].iloc[-1] < data['ADL'].iloc[-2]:
            return 'sell'
        else:
            return 'hold'