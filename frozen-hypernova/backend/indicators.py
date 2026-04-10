import pandas as pd
import numpy as np
import ta

def calculate_indicators(df):
    """
    Calculates all technical indicators required for the Hybrid Trading Strategy.
    
    Args:
        df (pd.DataFrame): DataFrame with columns 'open', 'high', 'low', 'close', 'volume'.
        
    Returns:
        pd.DataFrame: The original DataFrame enriched with indicator columns.
    """
    if df is None or len(df) == 0:
        return df
        
    # --- 1. Regime Filter: Average Directional Index (ADX) ---
    adx_indicator = ta.trend.ADXIndicator(high=df['high'], low=df['low'], close=df['close'], window=14)
    df['adx'] = adx_indicator.adx()
    
    # --- 2. Trend Strategy Indicators ---
    # Fast and Slow EMAs
    df['ema_50'] = ta.trend.ema_indicator(close=df['close'], window=50)
    df['ema_200'] = ta.trend.ema_indicator(close=df['close'], window=200)
    
    # MACD (Moving Average Convergence Divergence)
    macd_indicator = ta.trend.MACD(close=df['close'], window_slow=26, window_fast=12, window_sign=9)
    df['macd_line'] = macd_indicator.macd()
    df['macd_signal'] = macd_indicator.macd_signal()
    df['macd_hist'] = macd_indicator.macd_diff()
    
    # --- 3. Mean-Reversion Strategy Indicators ---
    # Bollinger Bands
    bb_indicator = ta.volatility.BollingerBands(close=df['close'], window=20, window_dev=2)
    df['bb_upper'] = bb_indicator.bollinger_hband()
    df['bb_lower'] = bb_indicator.bollinger_lband()
    df['bb_mid'] = bb_indicator.bollinger_mavg()
    
    # Relative Strength Index (RSI)
    df['rsi'] = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()
    
    # --- 4. Risk Management: Average True Range (ATR) ---
    df['atr'] = ta.volatility.AverageTrueRange(high=df['high'], low=df['low'], close=df['close'], window=14).average_true_range()
    
    # Drop rows with NaN values created by moving average lookback periods
    df.dropna(inplace=True)
    
    return df
