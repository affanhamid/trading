import logging
from datetime import datetime
from functools import wraps
from typing import Callable, Any

def get_current_date_log_filename(log_directory: str) -> str:
    """
    Generates a log filename based on the current date and specified directory.
    
    Args:
        log_directory (str): The directory where the log file will be stored.
    
    Returns:
        str: The path to the log file.
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    return f'{log_directory}/{current_date}.txt'

def log_rest_query(func: Callable) -> Callable:
    """
    Decorator to log REST API queries.
    
    Args:
        func (Callable): The function to be decorated.
    
    Returns:
        Callable: The wrapped function with logging.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        symbol = kwargs['symbol']
        log_filename = get_current_date_log_filename('logs/rest_queries')
        logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')
        logging.info(f"REST query for symbol: {symbol}")
        return func(*args, **kwargs)
    return wrapper

def log_buy_order(func: Callable) -> Callable:
    """
    Decorator to log buy orders.
    
    Args:
        func (Callable): The function to be decorated.
    
    Returns:
        Callable: The wrapped function with logging.
    """
    @wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        price = kwargs.get('price')
        time = kwargs.get('time')
        quantity = kwargs.get('quantity')
        log_filename = get_current_date_log_filename('logs/orders')
        with open(log_filename, 'a') as f:
            f.write(f'{time} Buy {quantity} @ {price} ')
        return func(self, *args, **kwargs)
    return wrapper

def log_sell_order(func: Callable) -> Callable:
    """
    Decorator to log sell orders.
    
    Args:
        func (Callable): The function to be decorated.
    
    Returns:
        Callable: The wrapped function with logging.
    """
    @wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        price = kwargs.get('price')
        time = kwargs.get('time')
        quantity = kwargs.get('quantity')
        last_bought = 0
        log_filename = get_current_date_log_filename('logs/orders')
        with open(log_filename, 'r') as f:
            last_bought = float(f.read().split('\n')[-1].split(' ')[4])
        with open(log_filename, 'a') as f:
            f.write(f'{time} Sell {quantity} @ {price} Profit = {round(float(price)*quantity - last_bought*quantity, 3)} ')
        return func(self, *args, **kwargs)
    return wrapper
