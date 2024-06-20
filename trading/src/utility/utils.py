from datetime import datetime
from functools import wraps
import os

def ensure_directory_exists(file_path: str):
    """
    Ensures that the directory for the given file path exists, creating it if necessary.
    
    Args:
        file_path (str): The full path including the filename where the directory existence needs to be checked.
    """
    directory_path = os.path.dirname(file_path)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def get_current_date_log_filename(log_directory: str) -> str:
    """Generates a log filename for the current date in the specified directory."""
    return f'{log_directory}/{datetime.now().strftime("%Y-%m-%d")}.txt'

def format_time_duration(seconds: int) -> str:
    """Formats seconds into a human-readable duration string."""
    if seconds % 3600 == 0:
        return f"{seconds // 3600}_hour"
    elif seconds % 60 == 0:
        return f"{seconds // 60}_min"
    elif seconds % 86400 == 0:
        return f"{seconds // 86400}_day"
    else:
        return f"{seconds}_sec"


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

