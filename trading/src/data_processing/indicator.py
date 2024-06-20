import pandas as pd

class Indicator:
    """
    A class used to calculate rolling high and low values of a price column in a DataFrame.

    Attributes
    ----------
    None

    Methods
    -------
    estimate_high_low(data, sliding_window=20)
        Calculates the rolling maximum and minimum of the 'price' column over a specified window size.
    """

    def __init__(self):
        """
        Initializes the Indicator class.
        """
        pass

    def estimate_high_low(self, data: pd.DataFrame, sliding_window: int = 20) -> pd.DataFrame:
        """
        Estimate rolling high and low prices in a DataFrame.

        Parameters:
        data (pd.DataFrame): DataFrame containing the price data.
        sliding_window (int): The number of periods to consider for calculating the rolling high and low.

        Returns:
        pd.DataFrame: The original DataFrame with two new columns 'high' and 'low' representing the rolling maximum and minimum prices.
        """
        data['high'] = data['price'].rolling(sliding_window).max()
        data['low'] = data['price'].rolling(sliding_window).min()
        return data

    def __str__(self):
        return self.__class__.__name__.split('.')[-1]
