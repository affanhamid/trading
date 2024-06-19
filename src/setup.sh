#!/bin/bash

# Update and install dependencies
sudo apt upgrade -y
sudo apt install python3 python3-pip build-essential python3-dev -y

# Creating the virtual environment
python3 -m venv myenv
source myenv/bin/activate

# Download and install TA-Lib
cd ~
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzvf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/usr
make
sudo make install

# Install requirements
pip install -r requirements.txt
