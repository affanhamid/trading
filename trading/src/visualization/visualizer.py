# import matplotlib.pyplot as plt
# from drawnow import drawnow
import pandas as pd
from typing import List

class Visualizer:
    def __init__(self, title = '', signals = []) -> None:
        """
        Initializes the Visualizer with default values.
        """
        self.data = None
        self.set_title(title)
        self.set_signals(signals)
    
    def set_data(self, data: pd.DataFrame) -> None:
        """
        Sets the data for the visualizer.
        
        Args:
            data (pd.DataFrame): The data to be set.
        """
        self.data = data

    def make_fig(self) -> None:
        """
        Creates the figure with subplots arranged in a grid for each list of signals.
        """
        num_groups = len(self.signals)
        # Define the number of rows and columns for the subplot grid
        num_cols = 2  # You can adjust this number based on your preference or dynamic calculation
        num_rows = (num_groups + num_cols - 1) // num_cols  # Ensures enough rows to hold all groups

        for i, signal_group in enumerate(self.signals, start=1):
            ax = plt.subplot(num_rows, num_cols, i)  # Create a subplot in the grid
            for signal in signal_group:
                if signal in self.data.columns:
                    ax.plot(self.data['time'], self.data[signal], label=signal)
            ax.set_title(f"{self.title} - {' & '.join(signal_group)}")
            ax.legend()
    
    def draw_graph(self) -> None:
        """
        Draws the graph using the make_fig method.
        """
        drawnow(self.make_fig)

    def set_signals(self, signals: List[str]) -> None:
        """
        Sets the signals to be plotted.
        
        Args:
            signals (List[str]): The list of signal names.
        """
        self.signals = signals

    def set_title(self, title: str) -> None:
        """
        Sets the title for the plots.
        
        Args:
            title (str): The title of the plots.
        """
        self.title = title

__all__ = ['Visualizer']