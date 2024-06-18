from Clients.rest_client import RESTClientWrapper
from Utility.logger import log_rest_query
from Visualization.visualizer import Visualizer
from Data_Processing.MACD import MACD
from Order_Management.order_manager import OrderManager
from Trading_Strategies.pure_macd import MACD_Strategy

import time
import pandas as pd

class RESTClientPoller:
    def __init__(self, strategy):
        self.wrapper = RESTClientWrapper()
        self.data = pd.DataFrame()
        self.visualizer = Visualizer()
        self.strategy = strategy
        
    def auto_update_data(func):
        def wrapper(self, *args, **kwargs):
            combined_data = func(self, *args, **kwargs)
            self.update_data_frame(combined_data, kwargs.get('persistence', 10))  # Default persistence to 10 if not provided
            return combined_data
        return wrapper

    @log_rest_query
    @auto_update_data
    def run_query(self, symbols, persistence=10):
        result = self.fetch_market_data(symbols)
        trade_details = self.extract_trade_details(result)
        market_info = self.extract_market_info(result)
        combined_data = {**trade_details, **market_info}
        return combined_data

    def run_query_on_interval(self, symbols, interval, show_graph, persistence, quantity=1):
        self.quantity = quantity
        while True:
            self.run_query(symbols=symbols, persistence=persistence)
            if show_graph:
                self.visualizer.draw_graph()
            time.sleep(interval)

    def fetch_market_data(self, symbols):
        return self.wrapper.client.get_market_trades(product_id=symbols, limit=1)

    def extract_trade_details(self, result):
        trade = result['trades'][0]
        return {
            'product_id': trade['product_id'],
            'price': float(trade['price']),
            'size': float(trade['size']),
            'time': pd.to_datetime(trade['time']),
            'side': trade['side']
        }

    def extract_market_info(self, result):
        return {
            'best_bid': float(result['best_bid']),
            'best_ask': float(result['best_ask'])
        }

    def update_data_frame(self, row, persistence):
        new_row = pd.DataFrame([row])
        self.data = pd.concat([self.data, new_row], ignore_index=True)
        self.visualize_data(row)
        self.run_strategy()

        if len(self.data) > persistence:
            self.data.drop(self.data.index[:-persistence], inplace=True)

    def visualize_data(self, row):
        self.visualizer.set_title(row['product_id'])
        self.visualizer.set_vars(['price', 'short_window', 'long_window'])
        self.visualizer.set_signals(['MACD', 'Signal'])
        self.visualizer.set_data(self.data)

    def run_strategy(self):
        self.strategy.process_data(self.data, self.quantity)
    
__all__ = ['RESTClientPoller']