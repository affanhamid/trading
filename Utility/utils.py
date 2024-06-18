import datetime
from functools import wraps

def calculate_brokerage_fee(func):
    """
    Decorator to calculate and log the brokerage fee for the last order of the day.
    
    Args:
        func (Callable): The function to be wrapped.
    
    Returns:
        Callable: The wrapped function with brokerage fee calculation.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        current_date: str = datetime.datetime.now().strftime("%Y-%m-%d")
        bought_price: float = 0.0
        sold_price: float = 0.0
        
        # Read the last line of the order log file for the current date
        with open(f'logs/orders/{current_date}.txt', 'r') as f:
            last_line: str = f.readlines()[-1]
            bought_price = float(last_line.split(' ')[4])
            sold_price = float(last_line.split(' ')[9])
            bought_quantity: float = float(last_line.split(' ')[2])
            sold_quantity: float = float(last_line.split(' ')[7])
        
        # Calculate the brokerage fee
        brokerage_fee: float = round(bought_price * bought_quantity * 0.012, 2) + round(sold_price * sold_quantity * 0.012, 2)
        
        # Append the brokerage fee to the order log file
        with open(f'logs/orders/{current_date}.txt', 'a') as f:
            f.write(f'Brokerage Fee: {brokerage_fee}\n')
    
    return wrapper