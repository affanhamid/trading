import pandas as pd
import talib as ta
from .indicator import Indicator

class StochasticOscillator(Indicator):
    def __init__(self, fastk_period: int = 14, slowk_period: int = 3, slowk_matype: int = 0, slowd_period: int = 3, slowd_matype: int = 0):
        self.fastk_period = fastk_period
        self.slowk_period = slowk_period
        self.slowk_matype = slowk_matype
        self.slowd_period = slowd_period
        self.slowd_matype = slowd_matype

    def calculate(self, data: pd.DataFrame) -> None:
        data = self.estimate_high_low(data)
        data['slowk'], data['slowd'] = ta.STOCH(data['high'], data['low'], data['price'], fastk_period=self.fastk_period, slowk_period=self.slowk_period, slowk_matype=self.slowk_matype, slowd_period=self.slowd_period, slowd_matype=self.slowd_matype)

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        last_row = data.iloc[-1]
        if last_row['slowk'] < 20 and last_row['slowd'] < 20:
            return 'buy'
        elif last_row['slowk'] > 80 and last_row['slowd'] > 80:
            return 'sell'
        else:
            return 'hold'