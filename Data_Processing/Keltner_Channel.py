import pandas as pd
import talib as ta
from Data_Processing.Indicator import Indicator


# Calculate the EMA of the close prices


# Calculate the upper and lower bands

class KeltnerChannel(Indicator):
    def __init__(self, time_period1: int = 20, time_period2: int = 10, nbdevup: int = 2, nbdevdn: int = 2):
        self.time_period1 = time_period1
        self.time_period2 = time_period2
        self.nbdevup = nbdevup
        self.nbdevdn = nbdevdn

    def calculate(self, data: pd.DataFrame) -> None:
        data = self.estimate_high_low(data)
        ema_close = ta.EMA(data['price'], timeperiod=self.time_period1)
        atr = ta.ATR(data['high'], data['low'], data['price'], timeperiod=self.time_period2)

        data['keltner_upper'] = ema_close + self.nbdevup * atr
        data['keltner_middle'] = ema_close
        data['keltner_lower'] = ema_close - self.nbdevdn * atr

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        last_row = data.iloc[-1]
        if last_row['price'] > last_row['keltner_upper']:
            return 'buy'
        elif last_row['price'] < last_row['keltner_lower']:
            return 'sell'
        else:
            return 'hold'
