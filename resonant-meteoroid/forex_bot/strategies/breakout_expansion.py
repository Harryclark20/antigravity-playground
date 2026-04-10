import pandas as pd

class BreakoutExpansionStrategy:
    def __init__(self, risk_reward_ratio=2.5, slow_atr_period=20, volume_ma_period=20):
        self.risk_reward_ratio = risk_reward_ratio
        self.slow_atr_period = slow_atr_period
        self.volume_ma_period = volume_ma_period

    def analyze(self, df: pd.DataFrame) -> dict:
        result = {
            'signal': 'NO_TRADE',
            'sl_price': 0.0,
            'sl_distance': 0.0,
            'tp_distance': 0.0,
            'confidence': 0.0,
            'weight': 1.0
        }
        if df is None or len(df) < max(self.slow_atr_period, self.volume_ma_period):
            return result

        current = df.iloc[-1]
        previous = df.iloc[-2]
        
        # Check if atr is increasing
        recent_atr_mean = df['ATR'].iloc[-self.slow_atr_period:-1].mean()
        atr_increasing = current['ATR'] > recent_atr_mean
        
        # Check volume spike
        if 'tick_volume' in df.columns:
            recent_vol_mean = df['tick_volume'].iloc[-self.volume_ma_period:-1].mean()
            vol_spike = current['tick_volume'] > (recent_vol_mean * 1.5)
        else:
            vol_spike = True # Fallback if volume not available
            
        # Breakout Donchian Upper
        breakout_up = current['close'] > previous['DC_upper'] 
        
        # Breakout Donchian Lower
        breakout_down = current['close'] < previous['DC_lower']

        if breakout_up and atr_increasing and vol_spike:
            result['signal'] = 'BUY'
            result['sl_price'] = current['DC_middle'] # Mid Donchian as dynamic support/ SL
            result['sl_distance'] = abs(current['close'] - result['sl_price'])
            if result['sl_distance'] < 0.0001:
                result['sl_distance'] = current['ATR'] # Fallback
            result['tp_distance'] = result['sl_distance'] * self.risk_reward_ratio
            result['confidence'] = 0.75
            return result
            
        if breakout_down and atr_increasing and vol_spike:
            result['signal'] = 'SELL'
            result['sl_price'] = current['DC_middle']
            result['sl_distance'] = abs(current['close'] - result['sl_price'])
            if result['sl_distance'] < 0.0001:
                result['sl_distance'] = current['ATR']
            result['tp_distance'] = result['sl_distance'] * self.risk_reward_ratio
            result['confidence'] = 0.75

        return result
