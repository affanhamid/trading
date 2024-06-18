import logging
from datetime import datetime
from functools import wraps
from typing import Callable, Any

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
        symbols = kwargs['symbols']
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_filename = f'logs/rest_queries/{current_date}.log'
        logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')
        logging.info(f"REST query for symbols: {symbols}")
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
        current_date = datetime.now().strftime("%Y-%m-%d")
        with open(f'logs/orders/{current_date}.txt', 'a') as f:
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
        current_date = datetime.now().strftime("%Y-%m-%d")
        # Read the last bought price from the log file
        with open(f'logs/orders/{current_date}.txt', 'r') as f:
            last_bought = float(f.read().split('\n')[-1].split(' ')[4])
        # Log the sell order with profit calculation
        with open(f'logs/orders/{current_date}.txt', 'a') as f:
            f.write(f'{time} Sell {quantity} @ {price} Profit = {round(float(price)*quantity - last_bought*quantity, 3)} ')
        return func(self, *args, **kwargs)
    return wrapper
