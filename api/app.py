from fastapi import FastAPI
from datetime import datetime
import pandas as pd

app = FastAPI()

@app.get("/data/")
async def get_data():
    file_path = 'logs/dataframes/data.csv'  # Adjust the path as necessary
    df = pd.read_csv(file_path)
    # Replace NaN values with None, which converts to null in JSON
    df_cleaned = df.fillna('null')
    return {"data": df_cleaned.to_dict(orient='records')}


def process_trade(trade):
    trade_data = trade.strip().split(' ')
    return {
        'bought_time': trade_data[0],
        'bought_amount': trade_data[2],
        'bought_at': trade_data[4],
        'sold_time': trade_data[5],
        'sold_amount': trade_data[7],
        'sold_at': trade_data[9],
        'profit': trade_data[12],
        'brokerage': trade_data[15],
    }


@app.get("/trades/all")
async def get_trades(number_of_trades: int = 50):
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_path = f'../logs/orders/{current_date}.txt'
    print(file_path)
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            trades_data = list(map(process_trade, lines))
    except FileNotFoundError:
        trades_data = ["No trades data found for today."]
    return {"data": trades_data}


@app.get("/trades/last/{number_of_trades}")
async def get_trades(number_of_trades: int = 50):
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_path = f'../logs/orders/{current_date}.txt'
    print(file_path)
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Get the last 'number_of_trades' lines
            last_trades = lines[-number_of_trades:]
            trades_data = list(map(process_trade, last_trades))
    except FileNotFoundError:
        trades_data = ["No trades data found for today."]
    return {"data": trades_data}
