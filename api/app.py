from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pandas as pd

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/data/")
async def get_data():
    file_path = 'logs/dataframes/data.csv'  # Adjust the path as necessary
    df = pd.read_csv(file_path)
    # Replace NaN values with None, which converts to null in JSON
    df_cleaned = df.fillna('null')
    return {"data": df_cleaned.to_dict(orient='records')}


def process_trade(trade):
    trade_data = trade.strip().split(' ')
    try:
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
    except IndexError:
        return "No trades data found for today."


@app.get("/trades/{date}")
async def get_trades(date: str):
    file_path = f'logs/orders/{date}.txt'
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            trades_data = list(map(process_trade, lines))
    except FileNotFoundError:
        trades_data = ["No trades data found for today."]
    return {"data": trades_data}
