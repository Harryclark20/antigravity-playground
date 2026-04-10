import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class PreciousMetalsVolatilityBreakoutStrategy:
    """
    Strategy 7: Precious Metals Volatility Breakout
    Environment: High Volatility Expansion (Trends)
    Asset Types: XAUUSD, GBPJPY, BTCUSD
    
    Logic:
    - Waits for the ATR to spike significantly above its moving average (Volatility Expansion).
    - Looks for a candle closing outside the Donchian Channel (Breakout Direction).
    - Confirms the move with EMAs (EMA 20 > EMA 50 for Buys, reverse for Sells).
    - Built specifically to catch massive intraday momentum bursts on metals.
    """
    
    def __init__(self, atr_multiplier=1.7):
        self.atr_multiplier = atr_multiplier
        logger.info("Initialized Precious Metals Volatility Breakout Strategy (High Selectivity)")

    def _calculate_atr_sma(self, df, period=14):
        # Calculate a simple moving average of the ATR to baseline volatility
        if 'ATR' not in df.columns:
            return pd.Series(np.nan, index=df.index)
        return df['ATR'].rolling(window=period).mean()

    def analyze(self, df: pd.DataFrame) -> dict:
        result = {
            'signal': 'NO_TRADE',
            'sl_distance': 0.0,
            'tp_distance': 0.0,
            'confidence': 0.0,
            'weight': 2.0,  # Strategy 7 has higher authority on these pairs
            'metadata': {}
        }

        if df is None or len(df) < 50:
            return result
            
        required_cols = ['close', 'high', 'low', 'ATR', 'DC_upper', 'DC_lower', 'EMA_20', 'EMA_50']
        if not all(col in df.columns for col in required_cols):
            return result

        # Get the latest data
        current_idx = df.index[-1]
        current_close = df.loc[current_idx, 'close']
        current_high = df.loc[current_idx, 'high']
        current_low = df.loc[current_idx, 'low']
        
        current_atr = df.loc[current_idx, 'ATR']
        atr_sma = self._calculate_atr_sma(df).iloc[-1]
        
        dc_upper = df.loc[current_idx, 'DC_upper']
        dc_lower = df.loc[current_idx, 'DC_lower']
        ema_20 = df.loc[current_idx, 'EMA_20']
        ema_50 = df.loc[current_idx, 'EMA_50']
        
        # 1. Volatility Expansion Check
        # Is the current ATR significantly higher than its recent average?
        if pd.isna(atr_sma) or current_atr < (atr_sma * self.atr_multiplier):
            return result
            
        # 2. Breakout Check
        bullish_breakout = current_close >= dc_upper
        bearish_breakout = current_close <= dc_lower
        
        # 3. EMA Trend Alignment
        uptrend = ema_20 > ema_50
        downtrend = ema_20 < ema_50
        
        # Generate Signals
        if bullish_breakout and uptrend:
            result['signal'] = 'BUY'
            # Wide SL for metals
            result['sl_distance'] = current_atr * 2.5
            # Catch the massive expansion move
            result['tp_distance'] = current_atr * 5.0
            result['confidence'] = 0.85
            
        elif bearish_breakout and downtrend:
            result['signal'] = 'SELL'
            result['sl_distance'] = current_atr * 2.5
            result['tp_distance'] = current_atr * 5.0
            result['confidence'] = 0.85
            
        result['metadata'] = {
            'current_atr': current_atr,
            'baseline_atr': atr_sma,
            'ema_alignment': 'UP' if uptrend else ('DOWN' if downtrend else 'FLAT')
        }

        return result
