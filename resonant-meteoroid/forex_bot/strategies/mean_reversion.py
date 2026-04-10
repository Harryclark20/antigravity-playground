import pandas as pd

class MeanReversionStrategy:
    def __init__(self, rsi_buy_threshold=30, rsi_sell_threshold=70, sl_atr_multiplier=1.2):
        self.rsi_buy_threshold = rsi_buy_threshold
        self.rsi_sell_threshold = rsi_sell_threshold
        self.sl_atr_multiplier = sl_atr_multiplier

    def analyze(self, df: pd.DataFrame) -> dict:
        result = {
            'signal': 'NO_TRADE',
            'sl_distance': 0.0,
            'tp_distance': 0.0,
            'confidence': 0.0,
            'weight': 1.0
        }
        if df is None or len(df) < 2:
            return result

        current = df.iloc[-1]
        
        # BUY Condition
        # Price touches lower Bollinger band (Low goes below or touches BB_lower)
        touch_lower_bb = current['low'] <= current['BB_lower']
        rsi_oversold = current['RSI'] < self.rsi_buy_threshold
        
        if touch_lower_bb and rsi_oversold:
            result['signal'] = 'BUY'
            result['sl_distance'] = current['ATR'] * self.sl_atr_multiplier
            result['tp_distance'] = abs(current['BB_middle'] - current['close'])
            result['confidence'] = 0.7
            return result
            
        # SELL Condition
        # Price touches upper Bollinger band
        touch_upper_bb = current['high'] >= current['BB_upper']
        rsi_overbought = current['RSI'] > self.rsi_sell_threshold
        
        if touch_upper_bb and rsi_overbought:
            result['signal'] = 'SELL'
            result['sl_distance'] = current['ATR'] * self.sl_atr_multiplier
            result['tp_distance'] = abs(current['BB_middle'] - current['close'])
            result['confidence'] = 0.7
            
        return result
