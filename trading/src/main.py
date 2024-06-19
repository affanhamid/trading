from data_collection.rest_client_poller import RESTClientPoller
# from Trading_Strategies.pure_macd import MACD_Strategy
from trading_strategies.MACD_RVI_AO import MACD_RVI_AO_Strategy

def main() -> None:
    """
    Main function to initialize the RESTClientPoller with MACD_Strategy
    and run the query on a specified interval.
    """
    # Initialize the poller with MACD strategy
    poller: RESTClientPoller = RESTClientPoller(MACD_RVI_AO_Strategy())
    
    # Run the query on interval with specified parameters
    poller.run_query_on_interval(
        symbol="BTC-USD", 
        interval=5, 
        show_graph=False, 
        persistence=60, 
        quantity=0.004
    )

if __name__ == "__main__":
    main()