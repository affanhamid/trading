from coinbase.rest import RESTClient
import os

class RESTClientWrapper:
    """
    A wrapper class for the Coinbase RESTClient to handle API interactions using environment variables for credentials.
    """
    def __init__(self):
        """
        Initializes the RESTClientWrapper instance by setting up the RESTClient with API credentials from environment variables.
        """
        # Retrieve API key and secret from environment variables
        api_key_name = os.getenv('COINBASE_API_NAME')
        api_key_secret = os.getenv('COINBASE_API_SECRET')
        
        # Initialize the RESTClient with the retrieved API credentials
        self.client = RESTClient(api_key=api_key_name, api_secret=api_key_secret)

__all__ = ['RESTClientWrapper']