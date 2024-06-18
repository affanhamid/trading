from Data_Processing.MACD import MACD
from Data_Processing.Advanced_Directional_Index import AverageDirectionalIndex
from Data_Processing.AD_Line import AccumulationDistributionLine
from Data_Processing.Average_True_Range import AverageTrueRange
from Data_Processing.Bollinger_Bands import BollingerBands
from Data_Processing.Commodity_Channel_index import CommodityChannelIndex
from Data_Processing.Ichimoku_Cloud import IchimokuCloud
from Data_Processing.Keltner_Channel import KeltnerChannel
from Data_Processing.Momentum import Momentum
from Data_Processing.Money_Flow_index import MoneyFlowIndex
from Data_Processing.Moving_Average import SimpleMovingAverage, ExponentialMovingAverage, WeightedMovingAverage
from Data_Processing.Parabolic_SAR import ParabolicSAR
from Data_Processing.Pivot_Points import PivotPoints
from Data_Processing.Rate_Of_Change import RateOfChange
from Data_Processing.RSI import RSI
from Data_Processing.Stochastic_Oscillator import StochasticOscillator
from Data_Processing.Williams_R import WilliamsR
from Data_Processing.Awesome_Indicator import AwesomeIndicator
from Data_Processing.Relative_Vigor_Index import RelativeVigorIndex

from .Strategy import Strategy
from pandas import DataFrame

class TestIndicator(Strategy):
    """A trading strategy class that uses MACD to determine buy or sell signals."""

    def __init__(self):
        """Initialize the MACD strategy with a MACD processor."""
        super().__init__([AwesomeIndicator])
        
    def process_data(self, data: DataFrame, quantity: int):
        """
        Process the given data to execute trading orders based on MACD signals using the superclass's method.

        Args:
            data (DataFrame): The market data.
            quantity (int): The amount to buy or sell.
        """
        print(super().process_data(data, quantity))
