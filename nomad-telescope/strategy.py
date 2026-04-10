import pandas as pd
import numpy as np
from ict_math import detect_fvg, detect_mss

class HybridStrategy:
    def __init__(self, symbol, htf="M15", ltf="M5"):
        self.symbol = symbol
        self.htf = htf
        self.ltf = ltf
        self.regime = "UNKNOWN"
        self.bias = "NEUTRAL"
        
    def _calculate_adx(self, df: pd.DataFrame, period=14):
        """Calculates Average Directional Index (ADX) to determine market regime."""
        df['tr1'] = df['high'] - df['low']
        df['tr2'] = abs(df['high'] - df['close'].shift(1))
        df['tr3'] = abs(df['low'] - df['close'].shift(1))
        df['tr'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
        
        df['plus_dm'] = np.where((df['high'] - df['high'].shift(1)) > (df['low'].shift(1) - df['low']), np.maximum(df['high'] - df['high'].shift(1), 0), 0)
        df['minus_dm'] = np.where((df['low'].shift(1) - df['low']) > (df['high'] - df['high'].shift(1)), np.maximum(df['low'].shift(1) - df['low'], 0), 0)
        
        atr = df['tr'].ewm(alpha=1/period, adjust=False).mean()
        df['plus_di'] = 100 * (df['plus_dm'].ewm(alpha=1/period, adjust=False).mean() / atr)
        df['minus_di'] = 100 * (df['minus_dm'].ewm(alpha=1/period, adjust=False).mean() / atr)
        
        dx = (abs(df['plus_di'] - df['minus_di']) / (df['plus_di'] + df['minus_di'])) * 100
        df['adx'] = dx.ewm(alpha=1/period, adjust=False).mean()
        
        return df['adx'].iloc[-1]

    def analyze_htf(self, df: pd.DataFrame):
        """Determines Regime (Trending vs Ranging) and Directional Bias."""
        if df.empty or len(df) < 50:
            return "UNKNOWN", "NEUTRAL"
            
        # 1. Determine Regime via ADX
        current_adx = self._calculate_adx(df, 14)
        if current_adx > 25:
            self.regime = "TRENDING"
        else:
            self.regime = "RANGING"
            
        # 2. Determine Bias via SMA for simple directional filter
        df['sma_200'] = df['close'].rolling(window=200).mean()
        last_close = df['close'].iloc[-1]
        last_sma = df['sma_200'].iloc[-1]
        
        if last_close > last_sma:
            self.bias = "BULLISH"
        elif last_close < last_sma:
            self.bias = "BEARISH"
        else:
            self.bias = "NEUTRAL"
            
        return self.regime, self.bias

    def find_ltf_entry(self, df: pd.DataFrame):
        """Routes the entry logic based on the current regime."""
        if df.empty or len(df) < 50:
            return None
            
        if self.regime == "TRENDING":
            return self._ict_momentum_logic(df)
        elif self.regime == "RANGING":
            return self._mean_reversion_logic(df)
        return None

    def _ict_momentum_logic(self, df: pd.DataFrame):
        """ICT FVG Breakout Engine (High RR, Lower WR)"""
        if self.bias == "NEUTRAL": return None
            
        df = detect_mss(df, lookback=3)
        df = detect_fvg(df, min_fvg_pips=2.0, point_size=0.0001) 
        
        last_candle = df.iloc[-1]
        prev_candle = df.iloc[-2]
        
        if self.bias == "BULLISH":
            if prev_candle['Bullish_FVG'] or last_candle['Bullish_FVG']:
                sl = df['low'].rolling(5).min().iloc[-1]
                risk = last_candle['close'] - sl
                tp = last_candle['close'] + (risk * 3) # 1:3 RR
                return {"signal": "BUY", "sl": sl, "tp": tp, "type": "ICT_TREND"}
                
        elif self.bias == "BEARISH":
            if prev_candle['Bearish_FVG'] or last_candle['Bearish_FVG']:
                sl = df['high'].rolling(5).max().iloc[-1]
                risk = sl - last_candle['close']
                tp = last_candle['close'] - (risk * 3) # 1:3 RR
                return {"signal": "SELL", "sl": sl, "tp": tp, "type": "ICT_TREND"}
                
        return None

    def _mean_reversion_logic(self, df: pd.DataFrame):
        """Bollinger/RSI Engine (Low RR, High WR)"""
        period = 20
        std_dev_multiplier = 2.2
        
        df['sma_20'] = df['close'].rolling(window=period).mean()
        df['std_dev'] = df['close'].rolling(window=period).std()
        df['upper_band'] = df['sma_20'] + (df['std_dev'] * std_dev_multiplier)
        df['lower_band'] = df['sma_20'] - (df['std_dev'] * std_dev_multiplier)
        
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi_14'] = 100 - (100 / (1 + rs))
        
        last_candle = df.iloc[-1]
        
        if last_candle['low'] <= last_candle['lower_band'] and last_candle['rsi_14'] < 30 and self.bias != "BEARISH":
            tp = last_candle['sma_20']
            risk_dist = tp - last_candle['close']
            sl = last_candle['close'] - (risk_dist * 2.5) # Inv RR
            if tp > last_candle['close']: 
                return {"signal": "BUY", "sl": sl, "tp": tp, "type": "MR_RANGE"}
                
        elif last_candle['high'] >= last_candle['upper_band'] and last_candle['rsi_14'] > 70 and self.bias != "BULLISH":
            tp = last_candle['sma_20']
            risk_dist = last_candle['close'] - tp
            sl = last_candle['close'] + (risk_dist * 2.5) # Inv RR
            if tp < last_candle['close']: 
                return {"signal": "SELL", "sl": sl, "tp": tp, "type": "MR_RANGE"}
                
        return None
