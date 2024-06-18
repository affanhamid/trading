import pandas as pd
import talib as ta
from .Indicator import Indicator


class RSI(Indicator):
    def __init__(self, time_period: int = 14):
        self.time_period = time_period

    def calculate(self, data: pd.DataFrame) -> None:
        data['RSI'] = ta.RSI(data['price'], timeperiod=self.time_period)

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        last_row = data.iloc[-1]
        if last_row['RSI'] < 30:
            return 'buy'
        elif last_row['RSI'] > 70:
            return 'sell'
        else:
            return 'hold'
