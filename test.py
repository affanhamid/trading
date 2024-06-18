import datetime

def calculate_net_profit():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    total_profit = 0.0
    total_brokerage = 0.0
    
    try:
        with open(f'logs/orders/{current_date}.txt', 'r') as f:
            for line in f:
                parts = line.strip().split(' ')
                if "Profit" in line and "Brokerage Fee" in line:
                    profit_index = parts.index("Profit") + 2
                    brokerage_index = parts.index("Fee:") + 1
                    total_profit += round(float(parts[profit_index]), 2)
                    total_brokerage += round(float(parts[brokerage_index]), 2)
    except FileNotFoundError:
        print(f"No log file found for {current_date}")
    
    net_profit = total_profit - total_brokerage
    print(f"Net Profit: {round(net_profit, 2)}, Total Profit: {round(total_profit, 2)}, Total Brokerage: {round(total_brokerage, 2)}")

calculate_net_profit()