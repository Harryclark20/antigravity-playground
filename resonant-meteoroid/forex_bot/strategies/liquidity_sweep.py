import pandas as pd
import numpy as np

class LiquiditySweepStrategy:
    def __init__(self, lookback=20, sweep_margin=0.0005):
        self.lookback = lookback
        self.sweep_margin = sweep_margin

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
        
        # Calculate recent swing highs and lows (excluding the current forming candle)
        history = df.iloc[-(self.lookback + 1):-1]
        recent_high = history['high'].max()
        recent_low = history['low'].min()
        
        # Find if there are 'equal' highs/lows. We approximate by checking if the 
        # highest high in the first half matches the highest high in the second half.
        # A simpler robust method: Did price just sweep the recent_high/low and reject?
        
        # Sweep High (Bearish Signal)
        swept_high = current['high'] > recent_high
        closed_below = current['close'] < recent_high
        bearish_pinbar = (current['high'] - max(current['open'], current['close'])) > abs(current['open'] - current['close']) * 1.5
        
        if swept_high and closed_below and bearish_pinbar:
            result['signal'] = 'SELL'
            result['sl_price'] = current['high'] + current['ATR'] * 0.5 # SL just above the sweep high
            # We can return TP as a generic 2x or 3x risk. The execution engine handles exact distance.
            result['sl_distance'] = abs(current['close'] - result['sl_price'])
            result['tp_distance'] = result['sl_distance'] * 2.5
            result['confidence'] = 0.75
            return result

        # Sweep Low (Bullish Signal)
        swept_low = current['low'] < recent_low
        closed_above = current['close'] > recent_low
        bullish_pinbar = (min(current['open'], current['close']) - current['low']) > abs(current['open'] - current['close']) * 1.5

        if swept_low and closed_above and bullish_pinbar:
            result['signal'] = 'BUY'
            result['sl_price'] = current['low'] - current['ATR'] * 0.5 # SL just below sweep low
            result['sl_distance'] = abs(current['close'] - result['sl_price'])
            result['tp_distance'] = result['sl_distance'] * 2.5
            result['confidence'] = 0.75

        return result
