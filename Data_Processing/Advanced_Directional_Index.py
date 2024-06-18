import pandas as pd
import talib as ta
from .Indicator import Indicator
import pandas as pd
import numpy as np

class AverageDirectionalIndex(Indicator):
    def __init__(self, timeperiod: int = 14):
        self.timeperiod = timeperiod
        super().__init__()

    def calculate(self, data: pd.DataFrame) -> None:
        data = self.estimate_high_low(data)
        data['ADX'] = ta.ADX(data['high'], data['low'], data['price'], timeperiod=self.timeperiod)

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        if data['ADX'].iloc[-1] > 25:
            return 'strong_trend'
        elif data['ADX'].iloc[-1] < 20:
            return 'weak_trend'
        else:
            return 'neutral'
