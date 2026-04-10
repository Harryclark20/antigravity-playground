from strategies.base import BaseStrategy

class MeanReversionStrategy(BaseStrategy):
    def __init__(self):
        super().__init__('mean_reversion')

    def prepare_data(self, df):
        df.ta.bbands(length=20, std=2.5, append=True) 
        df.ta.rsi(length=7, append=True) 
        df.ta.atr(length=14, append=True)

    def generate_signal(self, index, row, df_history):
        action = 'HOLD'
        entry = row['Close']
        sl = tp = 0.0

        rsi = row.get('RSI_7', 50)
        bb_lower = row.get('BBL_20_2.5', 0)
        bb_upper = row.get('BBU_20_2.5', float('inf'))
        bb_mid = row.get('BBM_20_2.5', 0)
        atr = row.get('ATRr_14', 0)

        if atr == 0: return {'action': 'HOLD'}

        # Extremely selective: RSI deeply oversold + price touched lower band, plus confirmation bounce
        if rsi < 25 and row['Close'] <= bb_lower + (atr * 0.1): # Close to lower band
            action = 'BUY'
            sl = row['Close'] - (atr * 1.0)
            tp = bb_mid + (atr * 0.5)  # Target above mid band
            entry = row['Close']

        elif rsi > 75 and row['Close'] >= bb_upper - (atr * 0.1):
            action = 'SELL'
            sl = row['Close'] + (atr * 1.0)
            tp = bb_mid - (atr * 0.5)
            entry = row['Close']

        return {'action': action, 'entry': entry, 'sl': sl, 'tp': tp}
