import pandas as pd
import talib as ta

class OnBalanceVolume:
    def calculate_obv(self, data: pd.DataFrame) -> None:
        data['OBV'] = ta.OBV(data['close'], data['volume'])