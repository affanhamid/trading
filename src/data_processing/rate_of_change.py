import pandas as pd
import talib as ta
from .indicator import Indicator

class RateOfChange(Indicator):
    def __init__(self, time_period: int = 10):
        self.time_period = time_period

    def calculate(self, data: pd.DataFrame) -> None:
        data['ROC'] = ta.ROC(data['price'], timeperiod=self.time_period)

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        last_row = data.iloc[-1]
        # Typical ROC trading strategy
        if last_row['ROC'] > 0:
            return 'buy'
        elif last_row['ROC'] < 0:
            return 'sell'
        else:
            return 'hold'
