from Data_Collection.rest_client_poller import RESTClientPoller
from Trading_Strategies.pure_macd import MACD_Strategy

if __name__ == "__main__":
    poller = RESTClientPoller(MACD_Strategy())
    poller.run_query_on_interval(symbols="BTC-USD", interval=1, show_graph = False, persistence=50, quantity=0.004)
