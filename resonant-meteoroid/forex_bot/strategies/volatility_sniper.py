import pandas as pd

class VolatilitySniperStrategy:
    def __init__(self, risk_reward=2.5, bb_narrow_margin=0.8, lookback=20):
        self.risk_reward = risk_reward
        self.bb_narrow_margin = bb_narrow_margin
        self.lookback = lookback

    def analyze(self, df: pd.DataFrame) -> dict:
        result = {
            'signal': 'NO_TRADE',
            'sl_price': 0.0,
            'sl_distance': 0.0,
            'tp_distance': 0.0,
            'confidence': 0.0,
            'weight': 1.0
        }
        if df is None or len(df) <= self.lookback:
            return result

        current = df.iloc[-1]
        previous = df.iloc[-2]
        
        # Check if BB bandwidth is narrowing before breakout
        recent_bb_mean = df['BB_bandwidth'].iloc[-self.lookback:-1].mean()
        bb_compress = previous['BB_bandwidth'] < (recent_bb_mean * self.bb_narrow_margin)
        
        # Check ATR declining before breakout
        recent_atr_mean = df['ATR'].iloc[-self.lookback:-1].mean()
        atr_decline = previous['ATR'] < recent_atr_mean
        
        # Vol spike on breakout
        if 'tick_volume' in df.columns:
            recent_vol_mean = df['tick_volume'].iloc[-self.lookback:-1].mean()
            vol_spike = current['tick_volume'] > (recent_vol_mean * 1.5)
        else:
            vol_spike = True

        # Breakout condition (closing outside recent structural range)
        range_high = df['high'].iloc[-self.lookback:-1].max()
        range_low = df['low'].iloc[-self.lookback:-1].min()

        bullish_breakout = current['close'] > range_high
        bearish_breakout = current['close'] < range_low
        
        if bb_compress and atr_decline and vol_spike and bullish_breakout:
            result['signal'] = 'BUY'
            result['sl_price'] = range_high - ((range_high - range_low) * 0.5) # Inside previous range
            result['sl_distance'] = abs(current['close'] - result['sl_price'])
            result['tp_distance'] = result['sl_distance'] * self.risk_reward
            result['confidence'] = 0.8
            return result

        if bb_compress and atr_decline and vol_spike and bearish_breakout:
            result['signal'] = 'SELL'
            result['sl_price'] = range_low + ((range_high - range_low) * 0.5)
            result['sl_distance'] = abs(current['close'] - result['sl_price'])
            result['tp_distance'] = result['sl_distance'] * self.risk_reward
            result['confidence'] = 0.8

        return result
