from data_processing.awesome_indicator import AwesomeIndicator
from data_processing.moving_average_convergance_divergence import MACD
from data_processing.relative_vigor_index import RelativeVigorIndex
from trading_strategies.strategy import Strategy
import pandas as pd

class MACD_RVI_AO_Strategy(Strategy):
    def __init__(self):
        """
        Initializes the MACD_RVI_AO_Strategy class which inherits from the Strategy class.
        This strategy uses MACD, Awesome Oscillator, and Relative Vigor Index indicators.
        """
        indicators = [MACD, AwesomeIndicator, RelativeVigorIndex]
        super().__init__(indicators=indicators)
        self.signals = pd.DataFrame({'MACD': [], 'AO': [], 'RVI': []})
        self.signals_to_graph = [['price', 'high', 'low'], ['AO'], ['MACD', 'MACD_Signal'], ['RVI', 'RVI_Signal']]

    def process_data(self, data: pd.DataFrame, quantity: int):
        """
        Processes the given market data to execute trading orders based on the combined signals
        from MACD, Awesome Oscillator, and Relative Vigor Index.

        Args:
            data (pd.DataFrame): The market data on which the trading decisions are based.
            quantity (int): The amount of the asset to buy or sell based on the trading signal.

        This method calculates the indicators, evaluates the signals, and places buy or sell orders
        based on the alignment of signals from the indicators.
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

            # Execute buy order if MACD and RVI signals agree and AO indicates a strong signal
            if (recent_signals_buy['MACD'] == recent_signals_buy['RVI']).any() and recent_signals_buy['AO'].iloc[-1] == 'strong signal':
                print('buy')
                self.add_order('buy', data, quantity)

            # Execute sell order if MACD and RVI signals agree and AO indicates a strong signal
            if (recent_signals_sell['MACD'] == recent_signals_sell['RVI']).any() and recent_signals_sell['AO'].iloc[-1] == 'strong signal':
                self.add_order('sell', data, quantity)
