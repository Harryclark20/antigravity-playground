import pandas as pd

class SessionMomentumStrategy:
    def __init__(self, rsi_buy_threshold=55, rsi_sell_threshold=45, london_start_hour=10, ny_end_hour=19):
        # Time constraints loosely mapped to MT5 EET broker time (common setup)
        # London opens ~10:00 broker time, NY closes ~19:00 broker time
        self.rsi_buy_threshold = rsi_buy_threshold
        self.rsi_sell_threshold = rsi_sell_threshold
        self.london_start_hour = london_start_hour
        self.ny_end_hour = ny_end_hour

    def _is_active_session(self, current_time) -> bool:
        if current_time is None:
            return True
        hour = current_time.hour
        return self.london_start_hour <= hour <= self.ny_end_hour

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
        previous = df.iloc[-2]
        
        # Check session time
        # Assuming index is datetime
        current_time = df.index[-1]
        if not self._is_active_session(current_time):
            return result

        # VWAP Condition
        price_above_vwap = current['close'] > current.get('VWAP', current['EMA_50'])  # Fallback to EMA50 if VWAP missing
        price_below_vwap = current['close'] < current.get('VWAP', current['EMA_50'])

        # EMA Trending
        ema_trending_up = current['EMA_20'] > previous['EMA_20']
        ema_trending_down = current['EMA_20'] < previous['EMA_20']

        # RSI Momentum
        rsi_bullish = current['RSI'] > self.rsi_buy_threshold
        rsi_bearish = current['RSI'] < self.rsi_sell_threshold

        if price_above_vwap and ema_trending_up and rsi_bullish:
            result['signal'] = 'BUY'
            result['sl_distance'] = current['ATR'] * 1.5
            result['tp_distance'] = result['sl_distance'] * 2.0
            result['confidence'] = 0.7
            return result
            
        if price_below_vwap and ema_trending_down and rsi_bearish:
            result['signal'] = 'SELL'
            result['sl_distance'] = current['ATR'] * 1.5
            result['tp_distance'] = result['sl_distance'] * 2.0
            result['confidence'] = 0.7

        return result
