import datetime
from functools import wraps

def calculate_brokerage_fee(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        bought_price = 0
        sold_price = 0
        with open(f'logs/orders/{current_date}.txt', 'r') as f:
            last_line = f.readlines()[-1]
            bought_price = float(last_line.split(' ')[4])
            sold_price = float(last_line.split(' ')[9])
            bought_quantity = float(last_line.split(' ')[2])
            sold_quantity = float(last_line.split(' ')[7])
        brokerage_fee = round(bought_price * bought_quantity * 0.012, 2) + round(sold_price * sold_quantity * 0.012, 2)
        with open(f'logs/orders/{current_date}.txt', 'a') as f:
            f.write(f'Brokerage Fee: {brokerage_fee}\n')
    return wrapper