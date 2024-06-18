from coinbase.rest import RESTClient
import os

class RESTClientWrapper:
    def __init__(self):
        api_key_name = os.getenv('COINBASE_API_NAME')
        api_key_secret = os.getenv('COINBASE_API_SECRET')
        self.client = RESTClient(api_key=api_key_name, api_secret=api_key_secret)

__all__ = ['RESTClientWrapper']