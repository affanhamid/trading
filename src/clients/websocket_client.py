from coinbase.websocket import WSClient
import os

class WebsocketClientWrapper:
    """
    A wrapper class for the Coinbase WebSocket client to handle real-time data via WebSocket.
    """
    def __init__(self, on_message):
        """
        Initializes the WebSocket client with API credentials and a message handler.

        Args:
            on_message (callable): The callback function to handle messages received from the WebSocket.
        """
        # Retrieve API credentials from environment variables
        api_key_name = os.getenv('COINBASE_API_NAME')
        api_key_secret = os.getenv('COINBASE_API_SECRET')
        
        # Initialize the WebSocket client with the API credentials and the specified message handler
        self.client = WSClient(api_key=api_key_name, api_secret=api_key_secret, on_message=on_message, on_open=lambda x: print('connection opened'))

__all__ = ['WebsocketClientWrapper']