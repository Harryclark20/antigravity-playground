from strategies.base import BaseStrategy

class ICTMomentumStrategy(BaseStrategy):
    def __init__(self):
        super().__init__('momentum')

    def prepare_data(self, df):
        df.ta.ema(length=9, append=True)
        df.ta.ema(length=21, append=True)
        df.ta.ema(length=50, append=True) # Macro trend
        df.ta.atr(length=14, append=True)
        df.ta.rsi(length=14, append=True)
        
    def generate_signal(self, index, row, df_history):
        action = 'HOLD'
        entry = row['Close']
        sl = tp = 0.0

        ema9 = row.get('EMA_9', 0)
        ema21 = row.get('EMA_21', 0)
        ema50 = row.get('EMA_50', 0)
        atr = row.get('ATRr_14', 0)
        rsi = row.get('RSI_14', 50)

        if not atr or ema50 == 0:
            return {'action': action}

        # Extremely Selective Trend Continuation Setup
        # 1. Macro trend must be established
        # 2. Fast EMAs aligned
        # 3. Pullback to EMA9 but closed above it
        # 4. RSI is in bullish/bearish continuation zone
        
        # BUY Setup
        if row['Close'] > ema50 and ema9 > ema21:
            if row['Low'] <= ema9 and row['Close'] > ema9 and 50 < rsi < 70:
                action = 'BUY'
                sl = row['Low'] - (atr * 0.5) 
                tp = row['High'] + (atr * 2.5) # High RR
                entry = row['Close']

        # SELL Setup
        elif row['Close'] < ema50 and ema9 < ema21:
            if row['High'] >= ema9 and row['Close'] < ema9 and 30 < rsi < 50:
                action = 'SELL'
                sl = row['High'] + (atr * 0.5)
                tp = row['Low'] - (atr * 2.5)
                entry = row['Close']

        return {'action': action, 'entry': entry, 'sl': sl, 'tp': tp}
