import logging
from datetime import datetime
from functools import wraps
from typing import Callable, Any
from utility.utils import get_current_date_log_filename, format_time_duration, ensure_directory_exists


def log_action(action_type: str, func: Callable) -> Callable:
    """Decorator to log buy or sell actions and calculate brokerage fees."""
    @wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        price = kwargs.get('price')
        time = kwargs.get('time')
        quantity = kwargs.get('quantity')
        interval = format_time_duration(int(kwargs.get('interval')))
        strategy = kwargs.get('strategy')
        log_filename = get_current_date_log_filename(f'logs/orders/{strategy}/{interval}')
        ensure_directory_exists(log_filename)
        
        taker_brokerage: float = 0.0035
        maker_brokerage: float = 0.0075
        brokerage_fee: float = 0.0

        if action_type == 'buy':
            log_message = f'{time} Buy {quantity} @ {price} '
            brokerage_fee = round(price * quantity * taker_brokerage, 2)
            with open(log_filename, 'a') as f:
                f.write(log_message)
        elif action_type == 'sell':
            last_bought = 0
            with open(log_filename, 'r') as f:
                last_bought = float(f.read().split('\n')[-1].split(' ')[4])
            profit = round(float(price) * quantity - last_bought * quantity, 3)
            log_message = f' {time} Sell {quantity} @ {price} Profit = {profit} '
            brokerage_fee = round(price * quantity * maker_brokerage, 2)
        
            with open(log_filename, 'a') as f:
                f.write(log_message + f'Brokerage Fee: {brokerage_fee}\n')
        return func(self, *args, **kwargs)
    return wrapper

def log_rest_query(func: Callable) -> Callable:
    """Decorator to log REST API queries."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        symbol = kwargs['symbol']
        log_filename = get_current_date_log_filename('logs/rest_queries')
        ensure_directory_exists(log_filename)
        logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')
        logging.info(f"REST query for symbol: {symbol}")
        return func(*args, **kwargs)
    return wrapper

def log_buy_order(func: Callable) -> Callable:
    """Decorator to log buy orders."""
    return log_action('buy', func)

def log_sell_order(func: Callable) -> Callable:
    """Decorator to log sell orders."""
    return log_action('sell', func)

def calculate_brokerage_fee(func: Callable) -> Callable:
    """Decorator to calculate and log the brokerage fee for the last order of the day."""
    @wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        result = func(self, *args, **kwargs)
        # Assume the brokerage fee is already calculated and logged in log_action
        return result
    return wrapper