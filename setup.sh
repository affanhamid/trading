#!/bin/bash

# Update and install dependencies
sudo apt upgrade -y
sudo apt install python3 python3-pip build-essential python3-dev tmux -y

# Creating the trading virtual environment
python3 -m venv trading_env
source trading_env/bin/activate

# Download and install TA-Lib
cd ~
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzvf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/usr
make
sudo make install

cd ~/trading

# Install requirements
source trading_env/bin/activate
pip install -r ./trading/requirements.txt


# Creating the api virtual environment
python3 -m venv api_env
source api_env/bin/activate

# Install requirements
pip install -r ./api/requirements.txt


# Start tmux session for trading app
tmux new-session -d -s trading_session
tmux send-keys -t trading_session "source trading_env/bin/activate" C-m
tmux send-keys -t trading_session "python3 trading/src/main.py" C-m

# Allow port 8000 to be public
sudo ufw allow 8000

# Start tmux session for API
tmux new-session -d -s api_session
tmux send-keys -t api_session "source api_env/bin/activate" C-m
tmux send-keys -t api_session "uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload" C-m