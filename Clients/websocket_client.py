from coinbase.websocket import WSClient
import os

class WebsocketClientWrapper:
    def __init__(self, on_message):
        api_key_name = os.getenv('COINBASE_API_NAME')
        api_key_secret = os.getenv('COINBASE_API_SECRET')
        self.client = WSClient(api_key=api_key_name, api_secret=api_key_secret, on_message=on_message, on_open=lambda x: print('connection opened'))

__all__ = ['WebsocketClientWrapper']