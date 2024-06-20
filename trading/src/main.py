from data_collection.rest_client_poller import RESTClientPoller
from trading_strategies.pure_indicator import PureIndicator
from data_processing.moving_average_convergance_divergence import MACD
from trading_strategies.MACD_RVI_AO import MACD_RVI_AO_Strategy
import sys

def main(symbol: str, interval: int, show_graph: bool, persistence: int, quantity: float, strategy_type: str) -> None:
    """
    Main function to initialize the RESTClientPoller with a specified strategy
    and run the query on a specified interval.
    """
    if strategy_type == "MACD":
        strategy = PureIndicator(MACD, interval)
    elif strategy_type == "MACD_RVI_AO":
        strategy = MACD_RVI_AO_Strategy(interval)
    else:
        raise ValueError("Unsupported strategy type")

    # Initialize the poller with the chosen strategy
    poller: RESTClientPoller = RESTClientPoller(strategy, interval=interval)
    
    # Run the query on interval with specified parameters
    poller.run_query_on_interval(
        symbol=symbol, 
        show_graph=show_graph, 
        persistence=persistence, 
        quantity=quantity
    )

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: main.py <symbol> <interval> <show_graph> <persistence> <quantity> <strategy_type>")
        sys.exit(1)
    symbol = sys.argv[1]
    interval = int(sys.argv[2])
    show_graph = sys.argv[3].lower() in ['true', '1', 't', 'y', 'yes']
    persistence = int(sys.argv[4])
    quantity = float(sys.argv[5])
    strategy_type = sys.argv[6]
    main(symbol, interval, show_graph, persistence, quantity, strategy_type)
