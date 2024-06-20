from data_collection.rest_client_poller import RESTClientPoller
from trading_strategies.pure_indicator import PureIndicator
from data_processing.moving_average_convergance_divergence import MACD
from trading_strategies.MACD_RVI_AO import MACD_RVI_AO_Strategy

def main() -> None:
    """
    Main function to initialize the RESTClientPoller with MACD_Strategy
    and run the query on a specified interval.
    """
    # Initialize the poller with MACD strategy
    poller: RESTClientPoller = RESTClientPoller(PureIndicator(MACD))
    
    # Run the query on interval with specified parameters
    poller.run_query_on_interval(
        symbol="BTC-USD", 
        interval=1, 
        show_graph=False, 
        persistence=60, 
        quantity=0.016
    )

if __name__ == "__main__":
    main()
