from Clients.rest_client import RESTClientWrapper
from Utility.logger import log_rest_query
from Visualization.visualizer import Visualizer
from Data_Processing.MACD import MACD
from Order_Management.order_manager import OrderManager
from Trading_Strategies.Strategy import Strategy

import time
import pandas as pd

class RESTClientPoller:
    """Class to poll REST API for market data and apply trading strategies."""
    
    def __init__(self, strategy: Strategy):
        """Initializes the poller with a trading strategy."""
        self.wrapper = RESTClientWrapper()  # REST client wrapper instance
        self.data = pd.DataFrame()  # DataFrame to store market data
        self.visualizer = Visualizer()  # Visualizer for data visualization
        self.strategy = strategy  # Trading strategy instance
        
    def auto_update_data(func):
        """Decorator to refresh the DataFrame after fetching data."""
        def wrapper(self, *args, **kwargs):
            combined_data = func(self, *args, **kwargs)
            # Update DataFrame with new data, default persistence is 10
            self.update_data_frame(combined_data, kwargs.get('persistence', 10))
            return combined_data
        return wrapper

    @log_rest_query
    @auto_update_data
    def run_query(self, symbols: str, persistence: int = 10) -> dict:
        """Fetches and processes market data for specified symbols."""
        result = self.fetch_market_data(symbols)
        trade_details = self.extract_trade_details(result)
        market_info = self.extract_market_info(result)
        combined_data = {**trade_details, **market_info}
        return combined_data

    def run_query_on_interval(self, symbols: str, interval: int, show_graph: bool, persistence: int, quantity: int = 1):
        """Executes queries repeatedly at specified intervals."""
        self.quantity = quantity
        while True:
            self.run_query(symbols=symbols, persistence=persistence)
            if show_graph:
                self.visualizer.draw_graph()
            time.sleep(interval)

    def fetch_market_data(self, symbols: str) -> dict:
        """Retrieves market data for given symbols."""
        return self.wrapper.client.get_market_trades(product_id=symbols, limit=1)

    def extract_trade_details(self, result: dict) -> dict:
        """Extracts and returns trade details from market data."""
        trade = result['trades'][0]
        return {
            'product_id': trade['product_id'],
            'price': float(trade['price']),
            'size': float(trade['size']),
            'time': pd.to_datetime(trade['time']),
            'side': trade['side']
        }

    def extract_market_info(self, result: dict) -> dict:
        """Extracts and returns market conditions from the data."""
        return {
            'best_bid': float(result['best_bid']),
            'best_ask': float(result['best_ask'])
        }

    def update_data_frame(self, row: dict, persistence: int):
        """Updates and trims the DataFrame to maintain data persistence."""
        new_row = pd.DataFrame([row])
        self.data = pd.concat([self.data, new_row], ignore_index=True)
        self.visualize_data(row)
        self.run_strategy()
        # print(self.data.tail())

        # Trim the DataFrame to the specified persistence length
        if len(self.data) > persistence:
            self.data.drop(self.data.index[:-persistence], inplace=True)

    def visualize_data(self, row: dict):
        """Updates visualization settings and data."""
        self.visualizer.set_title(row['product_id'])
        self.visualizer.set_signals([['price', 'high', 'low'], ['AO'], ['MACD', 'MACD_Signal'], ['RVI', 'RVI_Signal']])
        self.visualizer.set_data(self.data)

    def run_strategy(self):
        """Processes the latest market data using the trading strategy."""
        self.strategy.process_data(self.data, self.quantity)
    
__all__ = ['RESTClientPoller']