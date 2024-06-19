#!/bin/bash

# Update and install dependencies
sudo apt upgrade -y
sudo apt install python3 python3-pip build-essential python3-dev -y

# Creating the trading virtual environment
python3 -m venv trading_env
source trading_env/bin/activate

# Download and install TA-Lib
cd ~
# wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
# tar -xzvf ta-lib-0.4.0-src.tar.gz
mkdir ta-lib
cd ta-lib
# ./configure --prefix=/usr
# make
# sudo make install
cd ../trading

echo ls

# Install requirements
source trading_env/bin/activate
pip install -r ./trading/requirements.txt

nohup python3 trading/src/main.py > trading/logs/trading_bot.log 2>&1 &

# Creating the api virtual environment
python3 -m venv api_env
source api_env/bin/activate

# Install requirements
pip install -r ./api/requirements.txt

nohup uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload > api/logs/server.log 2>&1 &