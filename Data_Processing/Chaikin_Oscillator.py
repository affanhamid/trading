import pandas as pd
import talib as ta
from .Indicator import Indicator

# NEED VOLUMNE INFO

class ChaikinOscillator(Indicator):
    def __init__(self, fastperiod: int = 3, slowperiod: int = 10):
        self.fastperiod = fastperiod
        self.slowperiod = slowperiod

    def calculate_chaikin(self, data: pd.DataFrame) -> None:
        data = self.estimate_high_low(data)
        data['Chaikin'] = ta.ADOSC(data['high'], data['low'], data['close'], data['volume'], fastperiod=self.fastperiod, slowperiod=self.slowperiod)