import matplotlib.pyplot as plt
from drawnow import drawnow

def draw_graph(df):
    drawnow(make_fig, df)


class Visualizer:
    def __init__(self):
        self.data = None
        self.vars = None
        self.title = ''
    
    def set_data(self, data):
        self.data = data

    def make_fig(self):
        plt.subplot(2, 1, 1)  # First subplot for vars
        for var in self.vars:
            plt.plot(self.data['time'], self.data[var], label=var)
        plt.title(self.title)
        plt.legend()

        plt.subplot(2, 1, 2)  # Second subplot for signals
        for signal in self.signals:
            plt.plot(self.data['time'], self.data[signal], label=signal)
        plt.title(self.title + ' - Signals')
        plt.legend()

    def draw_graph(self):
        drawnow(self.make_fig)

    def set_vars(self, vars):
        self.vars = vars

    def set_signals(self, signals):
        self.signals = signals

    def set_title(self, title):
        self.title = title

__all__ = ['Visualizer']