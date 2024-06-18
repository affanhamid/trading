from Data_Processing.Awesome_Indicator import AwesomeIndicator
from Data_Processing.MACD import MACD
from Data_Processing.Relative_Vigor_Index import RelativeVigorIndex
from Trading_Strategies.Strategy import Strategy
import pandas as pd

class MACD_RVI_AO_Strategy(Strategy):
    def __init__(self):
        indicators = [MACD, AwesomeIndicator, RelativeVigorIndex]
        super().__init__(indicators=indicators)
        self.signals = pd.DataFrame({'MACD': [], 'AO': [], 'RVI': []})

    def process_data(self, data: pd.DataFrame, quantity: int):
        """
        Process the given data to execute trading orders based on MACD signals.

        Args:
            data (DataFrame): The market data.
            quantity (int): The amount to buy or sell.
        """
        for indicator in self.indicators:
            indicator.calculate(data)

        if data.shape[0] > 2:
            signals = [indicator.evaluate_signal(data) for indicator in self.indicators]
            self.signals = pd.concat([self.signals, pd.DataFrame({'MACD': [signals[0]], 'AO': [signals[1]], 'RVI': [signals[2]]})], ignore_index=True)

            recent_signals = self.signals.tail(5)
            print(signals)
            recent_signals_buy = recent_signals[recent_signals['MACD'] == 'buy']
            recent_signals_sell = recent_signals[recent_signals['MACD'] == 'sell']


            if (recent_signals_buy['MACD'] == recent_signals_buy['RVI']).any() and recent_signals_buy['AO'].iloc[-1] == 'strong signal':
                print('buy')
                self.add_order('buy', data, quantity)

            if (recent_signals_sell['MACD'] == recent_signals_sell['RVI']).any() and recent_signals_sell['AO'].iloc[-1] == 'strong signal':
                self.add_order('sell', data, quantity)

