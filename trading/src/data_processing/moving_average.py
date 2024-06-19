import pandas as pd
import talib as ta
from .indicator import Indicator

class SimpleMovingAverage(Indicator):
    def __init__(self, window_size: int = 20):
        self.window_size = window_size

    def calculate(self, data: pd.DataFrame) -> None:
        data[f'SMA_{self.window_size}'] = data['price'].rolling(window=self.window_size).mean()

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        last_row = data.iloc[-1]
        second_last_row = data.iloc[-2]
        sma_column = f'SMA_{self.window_size}'

        if second_last_row['price'] > second_last_row[sma_column] and last_row['price'] < last_row[sma_column]:
            return 'sell'
        elif second_last_row['price'] < second_last_row[sma_column] and last_row['price'] > last_row[sma_column]:
            return 'buy'
        else:
            return 'hold'

class ExponentialMovingAverage(Indicator):
    def __init__(self, window_size: int = 20):
        self.window_size = window_size

    def calculate(self, data: pd.DataFrame) -> None:
        data[f'EMA_{self.window_size}'] = ta.EMA(data['price'], timeperiod=self.window_size)

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        last_row = data.iloc[-1]
        second_last_row = data.iloc[-2]
        ema_column = f'EMA_{self.window_size}'

        if second_last_row['price'] > second_last_row[ema_column] and last_row['price'] < last_row[ema_column]:
            return 'sell'
        elif second_last_row['price'] < second_last_row[ema_column] and last_row['price'] > last_row[ema_column]:
            return 'buy'
        else:
            return 'hold'

class WeightedMovingAverage(Indicator):
    def __init__(self, window_size: int = 20):
        self.window_size = window_size

    def calculate(self, data: pd.DataFrame) -> None:
        data[f'WMA_{self.window_size}'] = ta.WMA(data['price'], timeperiod=self.window_size)

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        last_row = data.iloc[-1]
        second_last_row = data.iloc[-2]
        wma_column = f'WMA_{self.window_size}'

        if second_last_row['price'] > second_last_row[wma_column] and last_row['price'] < last_row[wma_column]:
            return 'sell'
        elif second_last_row['price'] < second_last_row[wma_column] and last_row['price'] > last_row[wma_column]:
            return 'buy'
        else:
            return 'hold'
