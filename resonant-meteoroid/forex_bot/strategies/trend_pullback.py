import pandas as pd

class TrendPullbackStrategy:
    def __init__(self, adx_threshold=20, sl_atr_multiplier=1.5, tp_sl_multiplier=2.0):
        self.adx_threshold = adx_threshold
        self.sl_atr_multiplier = sl_atr_multiplier
        self.tp_sl_multiplier = tp_sl_multiplier

    def analyze(self, df: pd.DataFrame) -> dict:
        """
        Analyzes the data and returns a signal dictionary.
        Signal can be 'BUY', 'SELL', or 'NO_TRADE'.
        """
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
        
        # Bullish candle confirmation: Close > Open
        bullish_candle = current['close'] > current['open']
        bearish_candle = current['close'] < current['open']
        
        # BUY Condition
        # Price above EMA200
        # Price touches/retraces near EMA50 (allow 0.1% margin for precision issues)
        price_near_ema50 = abs(current['low'] - current['EMA_50']) / current['EMA_50'] < 0.002 or current['low'] <= current['EMA_50'] <= current['high']
        is_uptrend = current['close'] > current['EMA_200']
        rsi_buy_zone = 35 <= current['RSI'] <= 45
        adx_strong = current['ADX'] > self.adx_threshold
        
        if is_uptrend and price_near_ema50 and rsi_buy_zone and adx_strong and bullish_candle:
            result['signal'] = 'BUY'
            result['sl_distance'] = current['ATR'] * self.sl_atr_multiplier
            result['tp_distance'] = result['sl_distance'] * self.tp_sl_multiplier
            result['confidence'] = 0.8
            return result
            
        # SELL Condition
        # Price below EMA200
        # Price touches/retraces near EMA50
        price_near_ema50_sell = abs(current['high'] - current['EMA_50']) / current['EMA_50'] < 0.002 or current['low'] <= current['EMA_50'] <= current['high']
        is_downtrend = current['close'] < current['EMA_200']
        rsi_sell_zone = 55 <= current['RSI'] <= 65
        
        if is_downtrend and price_near_ema50_sell and rsi_sell_zone and adx_strong and bearish_candle:
            result['signal'] = 'SELL'
            result['sl_distance'] = current['ATR'] * self.sl_atr_multiplier
            result['tp_distance'] = result['sl_distance'] * self.tp_sl_multiplier
            result['confidence'] = 0.8
            
        return result
