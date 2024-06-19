import pandas as pd
import talib as ta
from .indicator import Indicator

# DONT HAVE VOLUMNE INFO

class AccumulationDistributionLine(Indicator):
    """
    A class used to calculate the Accumulation/Distribution Line (ADL) indicator.

    Methods
    -------
    calculate(data: pd.DataFrame) -> None
        Calculates the ADL and adds it to the DataFrame.
    
    evaluate_signal(data: pd.DataFrame) -> str
        Evaluates the ADL to generate a trading signal ('buy', 'sell', or 'hold').
    """
    
    def calculate(self, data: pd.DataFrame) -> None:
        """
        Calculates the Accumulation/Distribution Line (ADL) and adds it to the DataFrame.

        Parameters
        ----------
        data : pd.DataFrame
            A DataFrame containing the columns 'high', 'low', 'price', and 'volume'.
        """
        data = self.estimate_high_low(data)
        data['ADL'] = ta.AD(data['high'], data['low'], data['price'], data['volume'])

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        """
        Evaluates the ADL to generate a trading signal.

        Parameters
        ----------
        data : pd.DataFrame
            A DataFrame containing the 'ADL' column.

        Returns
        -------
        str
            A trading signal: 'buy' if the ADL is increasing, 'sell' if it is decreasing, or 'hold' if it is unchanged.
        """
        if data['ADL'].iloc[-1] > data['ADL'].iloc[-2]:
            return 'buy'
        elif data['ADL'].iloc[-1] < data['ADL'].iloc[-2]:
            return 'sell'
        else:
            return 'hold'