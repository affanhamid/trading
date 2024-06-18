import pandas as pd

class Indicator:
    def __init__(self):
        pass

    def estimate_high_low(self, data: pd.DataFrame, sliding_window:int = 20) -> pd.DataFrame:
        data['high'] = data['price'].rolling(sliding_window).max()
        data['low'] = data['price'].rolling(sliding_window).min()
        return data