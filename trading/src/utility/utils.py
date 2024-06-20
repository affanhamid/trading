from datetime import datetime
from functools import wraps

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


def calculate_net_profit() -> None:
    """
    Calculate and print the net profit by reading the log file for the current date.
    """
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    total_profit = 0.0
    total_brokerage = 0.0
    
    try:
        # Open the log file for the current date
        with open(f'logs/orders/{current_date}.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(' ')
                # Check if the line contains both "Profit" and "Brokerage Fee"
                if "Profit" in line and "Brokerage Fee" in line:
                    profit_index = parts.index("Profit") + 2
                    brokerage_index = parts.index("Fee:") + 1
                    total_profit += round(float(parts[profit_index]), 2)
                    total_brokerage += round(float(parts[brokerage_index]), 2)
    except FileNotFoundError:
        print(f"No log file found for {current_date}")
    
    net_profit = total_profit - total_brokerage
    # Print the calculated net profit, total profit, and total brokerage
    return (f"Net Profit: {round(net_profit, 2)}, Total Profit: {round(total_profit, 2)}, Total Brokerage: {round(total_brokerage, 2)}")

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
        bought_price: float = 0.0
        sold_price: float = 0.0
        taker_brokerage: float = 0.0035
        maker_brokerage: float = 0.0075
        
        # Read the last line of the order log file for the current date
        log_filename = get_current_date_log_filename('logs/orders')
        with open(log_filename, 'r') as f:
            last_line: str = f.readlines()[-1]
            bought_price = float(last_line.split(' ')[4])
            sold_price = float(last_line.split(' ')[9])
            bought_quantity: float = float(last_line.split(' ')[2])
            sold_quantity: float = float(last_line.split(' ')[7])
        
        # Calculate the brokerage fee
        brokerage_fee: float = round(round(bought_price * bought_quantity * taker_brokerage, 2) + round(sold_price * sold_quantity * maker_brokerage, 2), 2)

        log_filename = get_current_date_log_filename('logs/orders')
        
        # Append the brokerage fee to the order log file
        with open(log_filename, 'a') as f:
            f.write(f'Brokerage Fee: {brokerage_fee}\n')
    
    return wrapper