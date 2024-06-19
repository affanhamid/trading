import pandas as pd
from .indicator import Indicator

class MACD(Indicator):
    def __init__(self, short_span: int = 12, long_span: int = 26, signal_span: int = 9):
        """
        Constructor for the MACD class, setting up the parameters for the moving average convergence divergence calculation.

        Parameters:
            short_span (int): The number of periods to use for the short-term exponential moving average (EMA).
            long_span (int): The number of periods to use for the long-term exponential moving average (EMA).
            signal_span (int): The number of periods to use for the signal line, which is an EMA of the MACD line.

        The MACD line is calculated by subtracting the long-term EMA from the short-term EMA. The signal line is then
        calculated as an EMA of the MACD line.
        """
        self.short_span = short_span
        self.long_span = long_span
        self.signal_span = signal_span

    def calculate(self, data: pd.DataFrame) -> None:
        """
        Computes the MACD line and the signal line using the price data provided.

        Parameters:
            data (pd.DataFrame): A DataFrame with a 'price' column from which the EMAs and MACD values will be computed.

        This method modifies the input DataFrame by adding two new columns:
        - 'short_window': The short-term EMA of the price.
        - 'long_window': The long-term EMA of the price.
        - 'MACD': The MACD line, which is the difference between the short-term and long-term EMAs.
        - 'MACD_Signal': The signal line, which is an EMA of the MACD line.
        """
        # Calculate short-term EMA
        data['short_window'] = data['price'].ewm(span=self.short_span, adjust=False).mean()
        # Calculate long-term EMA
        data['long_window'] = data['price'].ewm(span=self.long_span, adjust=False).mean()

        # Calculate MACD
        data['MACD'] = data['short_window'] - data['long_window']
        # Calculate Signal line
        data['MACD_Signal'] = data['MACD'].ewm(span=self.signal_span, adjust=False).mean()

    def evaluate_signal(self, data: pd.DataFrame) -> str:
        """
        Determines the trading signal ('buy', 'sell', or 'hold') based on the crossover of the MACD line and the signal line.

        Parameters:
            data (pd.DataFrame): A DataFrame containing the calculated MACD and signal line values.

        Returns:
            str: A trading signal:
            - 'buy' if the MACD line crosses above the signal line.
            - 'sell' if the MACD line crosses below the signal line.
            - 'hold' if there is no crossover.

        The function checks the last two rows of the DataFrame to determine if a crossover occurred.
        """
        # Get the last two rows of data
        last_row = data.iloc[-1]
        second_last_row = data.iloc[-2]

        # Determine the trading signal
        if (second_last_row['MACD'] > second_last_row['MACD_Signal'] and last_row['MACD'] < last_row['MACD_Signal']):
            return 'sell'
        elif (second_last_row['MACD'] < second_last_row['MACD_Signal'] and last_row['MACD'] > last_row['MACD_Signal']):
            return 'buy'
        else:
            return 'hold'
