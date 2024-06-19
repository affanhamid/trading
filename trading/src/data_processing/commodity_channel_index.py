import pandas as pd
import talib as ta
from .indicator import Indicator

class CommodityChannelIndex(Indicator):
    def __init__(self, timeperiod: int = 20):
        self.timeperiod = timeperiod

    def calculate(self, data: pd.DataFrame) -> None:
        data = self.estimate_high_low(data)
        data['CCI'] = ta.CCI(data['high'], data['low'], data['price'], timeperiod=self.timeperiod)

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        cci = data['CCI'].iloc[-1]
        if cci > 100:
            return 'sell'
        elif cci < -100:
            return 'buy'
        else:
            return 'hold'
