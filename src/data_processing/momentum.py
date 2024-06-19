import pandas as pd
import talib as ta
from .indicator import Indicator

class Momentum(Indicator):
    def __init__(self, time_period: int = 10):
        self.time_period = time_period

    def calculate(self, data: pd.DataFrame) -> None:
        data['MOM'] = ta.MOM(data['price'], timeperiod=self.time_period)

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        last_row = data.iloc[-1]
        second_last_row = data.iloc[-2]

        # Determine the trading signal
        if second_last_row['MOM'] < 0 and last_row['MOM'] > 0:
            return 'buy'
        elif second_last_row['MOM'] > 0 and last_row['MOM'] < 0:
            return 'sell'
        else:
            return 'hold'
