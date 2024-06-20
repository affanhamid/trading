from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pandas as pd
import uvicorn
import os

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

@app.get("/strategies")
async def get_strategies():
    base_path = 'logs/dataframes'
    strategies = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    return {"strategies": strategies}

@app.get("/timeframes/{strategy}")
async def get_timeframes(strategy: str):
    base_path = f'logs/dataframes/{strategy}'
    if os.path.exists(base_path) and os.path.isdir(base_path):
        timeframes = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        return {"timeframes": timeframes}
    else:
        return {"error": "Strategy not found"}, 404


@app.get("/data/{strategy}/{timeframe}")
async def get_data(strategy: str, timeframe: str):
    file_path = f'logs/dataframes/{strategy}/{timeframe}/data.csv'  # Adjust the path as necessary
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


@app.get("/trades/{strategy}/{timeframe}/{date}")
async def get_trades(strategy: str, timeframe: str, date: str):
    file_path = f'logs/orders/{strategy}/{timeframe}/{date}.txt'
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            trades_data = list(map(process_trade, lines))
    except FileNotFoundError:
        trades_data = ["No trades data found for today."]
    return {"data": trades_data}


if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000, ssl_keyfile="/etc/letsencrypt/live/affanhamid.com/privkey.pem", ssl_certfile="/etc/letsencrypt/live/affanhamid.com/fullchain.pem")
    uvicorn.run(app, host="0.0.0.0", port=8000)