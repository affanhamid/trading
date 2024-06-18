import pandas as pd
import talib as ta
from .Indicator import Indicator

# NEED VOLUME DATA

class MoneyFlowIndex(Indicator):
    def __init__(self, timeperiod: int = 14):
        self.timeperiod = timeperiod

    def calculate(self, data: pd.DataFrame) -> None:
        data = self.estimate_high_low(data)
        data['MFI_14'] = ta.MFI(data['high'], data['low'], data['price'], data['volume'], timeperiod=self.timeperiod)