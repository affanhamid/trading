class MACD:
    def __init__(self, short_span=12, long_span=26, signal_span=9):
        self.short_span = short_span
        self.long_span = long_span
        self.signal_span = signal_span

    def calculate_macd(self, data):
        data['short_window'] = data['price'].ewm(span=self.short_span, adjust=False).mean()
        data['long_window'] = data['price'].ewm(span=self.long_span, adjust=False).mean()
        data['MACD'] = data['short_window'] - data['long_window']
        data['Signal'] = data['MACD'].ewm(span=self.signal_span, adjust=False).mean()

    def evaluate_signal(self, data):
        last_row = data.iloc[-1]
        second_last_row = data.iloc[-2]

        if (second_last_row['MACD'] > second_last_row['Signal'] and last_row['MACD'] < last_row['Signal']):
            return 'sell'
        elif (second_last_row['MACD'] < second_last_row['Signal'] and last_row['MACD'] > last_row['Signal']):
            return 'buy'
        else:
            return 'hold'
