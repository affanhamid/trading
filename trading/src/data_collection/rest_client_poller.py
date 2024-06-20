from clients.rest_client import RESTClientWrapper
from visualization.visualizer import Visualizer
from order_management.order_manager import OrderManager
from trading_strategies.strategy import Strategy
from utility.utils import format_time_duration, ensure_directory_exists
import time
import pandas as pd
import os

class RESTClientPoller:
    """
    A class responsible for polling REST API to fetch market data and applying trading strategies based on the data.
    
    Attributes:
        wrapper (RESTClientWrapper): An instance of RESTClientWrapper to interact with REST API.
        data (DataFrame): A pandas DataFrame to store the fetched market data.
        visualizer (Visualizer): An instance of Visualizer to visualize the data.
        strategy (Strategy): An instance of Strategy to apply trading strategies on the data.
    """
    
    def __init__(self, strategy: Strategy, interval: int):
        """
        Initializes the RESTClientPoller with a specific trading strategy.
        
        Args:
            strategy (Strategy): The trading strategy to be used with the poller.
        """
        self.wrapper = RESTClientWrapper()  # REST client wrapper instance
        self.data = pd.DataFrame()  # DataFrame to store market data
        self.visualizer = Visualizer(signals = strategy.signals_to_graph)  # Visualizer for data visualization
        self.strategy = strategy  # Trading strategy instance
        self.interval = interval
        
    def auto_update_data(func):
        """
        A decorator to automatically update the DataFrame after fetching new data.
        
        Args:
            func (function): The function to wrap.
        
        Returns:
            function: The wrapper function.
        """
        def wrapper(self, *args, **kwargs):
            combined_data = func(self, *args, **kwargs)
            # Update DataFrame with new data, default persistence is 10
            self.update_data_frame(combined_data, kwargs.get('persistence', 10))
            return combined_data
        return wrapper

    def save_data_to_file(self):
        """
        Saves the current DataFrame to a CSV file.

        This method will export the `data` attribute, which contains the market data,
        to a CSV file located at a predefined path. The index of the DataFrame is not
        included in the CSV file.
        """
        file_path = f'logs/dataframes/{self.strategy.__str__()}/{format_time_duration(self.interval)}/data.csv'
        ensure_directory_exists(file_path)
        self.data.to_csv(file_path, index=False)

    @auto_update_data
    def run_query(self, symbol: str, persistence: int = 10) -> dict:
        """
        Fetches and processes market data for a specified symbol.
        
        Args:
            symbol (str): The market symbol to query data for.
            persistence (int): The number of data points to persist in the DataFrame.
        
        Returns:
            dict: A dictionary containing combined trade details and market information.
        """
        result = self.fetch_market_data(symbol)
        trade_details = self.extract_trade_details(result)
        market_info = self.extract_market_info(result)
        combined_data = {**trade_details, **market_info}
        return combined_data

    def run_query_on_interval(self, symbol: str, show_graph: bool, persistence: int, quantity: int = 1):
        """
        Periodically executes queries at specified intervals and optionally displays a graph.
        
        Args:
            symbol (str): The market symbol to query data for.
            interval (int): The interval in seconds between queries.
            show_graph (bool): Whether to display the graph after each query.
            persistence (int): The number of data points to persist in the DataFrame.
            quantity (int): The quantity to be used in trading strategies.
        """
        self.quantity = quantity
        self.visualizer.set_title(symbol)
        while True:
            self.run_query(symbol=symbol, persistence=persistence)
            if show_graph:
                self.visualizer.draw_graph()
            time.sleep(self.interval)

    def fetch_market_data(self, symbol: str) -> dict:
        """
        Retrieves market data for a given symbol.
        
        Args:
            symbol (str): The market symbol to fetch data for.
        
        Returns:
            dict: The market data retrieved from the API.
        """
        return self.wrapper.client.get_market_trades(product_id=symbol, limit=1)

    def extract_trade_details(self, result: dict) -> dict:
        """
        Extracts trade details from the market data.
        
        Args:
            result (dict): The market data from which to extract trade details.
        
        Returns:
            dict: A dictionary containing key trade details.
        """
        trade = result['trades'][0]
        return {
            'product_id': trade['product_id'],
            'price': float(trade['price']),
            'size': float(trade['size']),
            'time': pd.to_datetime(trade['time']),
            'side': trade['side']
        }

    def extract_market_info(self, result: dict) -> dict:
        """
        Extracts market conditions from the data.
        
        Args:
            result (dict): The market data from which to extract market conditions.
        
        Returns:
            dict: A dictionary containing key market conditions.
        """
        return {
            'best_bid': float(result['best_bid']),
            'best_ask': float(result['best_ask'])
        }

    def update_data_frame(self, row: dict, persistence: int):
        """
        Updates and trims the DataFrame to maintain a specified number of data points.
        
        Args:
            row (dict): The new data row to add to the DataFrame.
            persistence (int): The number of data points to persist in the DataFrame.
        """
        new_row = pd.DataFrame([row])
        if len(self.data) >= persistence:
            self.data = self.data.iloc[1:].reset_index(drop=True)
        self.data = pd.concat([self.data, new_row], ignore_index=True)
        self.save_data_to_file()
        self.visualizer.set_data(self.data)
        self.run_strategy()

    def run_strategy(self):
        """
        Processes the latest market data using the assigned trading strategy.
        """
        self.strategy.process_data(self.data, self.quantity)
    
__all__ = ['RESTClientPoller']