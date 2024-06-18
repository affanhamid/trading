import pandas as pd

class MACD:
    def __init__(self, short_span: int = 12, long_span: int = 26, signal_span: int = 9):
        """
        Initializes the MACD class with given spans for short, long, and signal windows.

        Args:
            short_span (int): Span for the short-term EMA.
            long_span (int): Span for the long-term EMA.
            signal_span (int): Span for the signal line EMA.
        """
        self.short_span = short_span
        self.long_span = long_span
        self.signal_span = signal_span

    def calculate_macd(self, data: pd.DataFrame) -> None:
        """
        Calculates the MACD and Signal line for the given data.

        Args:
            data (pd.DataFrame): DataFrame containing price data.
        """
        # Calculate short-term EMA
        data['short_window'] = data['price'].ewm(span=self.short_span, adjust=False).mean()
        # Calculate long-term EMA
        data['long_window'] = data['price'].ewm(span=self.long_span, adjust=False).mean()
        
        # Calculate MACD
        data['MACD'] = data['short_window'] - data['long_window']
        # Calculate Signal line
        data['Signal'] = data['MACD'].ewm(span=self.signal_span, adjust=False).mean()

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        """
        Evaluates the trading signal based on the MACD and Signal line.

        Args:
            data (pd.DataFrame): DataFrame containing MACD and Signal line data.

        Returns:
            str: 'buy', 'sell', or 'hold' based on the MACD crossover strategy.
        """
        # Get the last two rows of data
        last_row = data.iloc[-1]
        second_last_row = data.iloc[-2]

        # Determine the trading signal
        if (second_last_row['MACD'] > second_last_row['Signal'] and last_row['MACD'] < last_row['Signal']):
            return 'sell'
        elif (second_last_row['MACD'] < second_last_row['Signal'] and last_row['MACD'] > last_row['Signal']):
            return 'buy'
        else:
            return 'hold'
