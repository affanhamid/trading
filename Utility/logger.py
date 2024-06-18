import logging
from datetime import datetime
from functools import wraps

def log_rest_query(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        symbols = kwargs['symbols']
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_filename = f'logs/rest_queries/{current_date}.log'
        logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')
        logging.info(f"REST query for symbols: {symbols}")
        return func(*args, **kwargs)
    return wrapper


def log_buy_order(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        price = kwargs.get('price')
        time = kwargs.get('time')
        quantity = kwargs.get('quantity')
        current_date = datetime.now().strftime("%Y-%m-%d")
        with open(f'logs/orders/{current_date}.txt', 'a') as f:
            f.write(f'{time} Buy {quantity} @ {price} ')
        return func(self, *args, **kwargs)
    return wrapper

def log_sell_order(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        price = kwargs.get('price')
        time = kwargs.get('time')
        quantity = kwargs.get('quantity')
        last_bought = 0
        current_date = datetime.now().strftime("%Y-%m-%d")
        with open(f'logs/orders/{current_date}.txt', 'r') as f:
            last_bought = float(f.read().split('\n')[-1].split(' ')[4])
        with open(f'logs/orders/{current_date}.txt', 'a') as f:
            f.write(f'{time} Sell {quantity} @ {price} Profit = {round(float(price) - last_bought, 3)} ')
        return func(self, *args, **kwargs)
    return wrapper
