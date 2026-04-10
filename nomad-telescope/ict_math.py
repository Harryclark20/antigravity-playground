import pandas as pd
import numpy as np

def calculate_swing_highs_lows(df: pd.DataFrame, lookback: int = 5) -> pd.DataFrame:
    """Identifies swing highs and lows based on a lookback period."""
    if df.empty or len(df) < lookback * 2 + 1:
        df['Swing_High'] = False
        df['Swing_Low'] = False
        return df

    df['Swing_High'] = df['high'] == df['high'].rolling(window=lookback * 2 + 1, center=True).max()
    df['Swing_Low'] = df['low'] == df['low'].rolling(window=lookback * 2 + 1, center=True).min()
    return df

def detect_fvg(df: pd.DataFrame, min_fvg_pips: float = 2.0, point_size: float = 0.0001) -> pd.DataFrame:
    """
    Detects Bullish and Bearish Fair Value Gaps (FVG).
    A bullish FVG occurs when the low of candle 3 is higher than the high of candle 1.
    A bearish FVG occurs when the high of candle 3 is lower than the low of candle 1.
    """
    if df.empty or len(df) < 3:
        df['Bullish_FVG'] = False
        df['Bearish_FVG'] = False
        return df

    # Shift to get previous candles
    df['high_shift_2'] = df['high'].shift(2)
    df['low_shift_2'] = df['low'].shift(2)

    # Bullish FVG: low[i] > high[i-2]
    bullish_fvg_cond = df['low'] > df['high_shift_2']
    # Size check
    bullish_size = (df['low'] - df['high_shift_2']) / point_size
    df['Bullish_FVG'] = bullish_fvg_cond & (bullish_size >= min_fvg_pips)

    # Bearish FVG: high[i] < low[i-2]
    bearish_fvg_cond = df['high'] < df['low_shift_2']
    # Size check
    bearish_size = (df['low_shift_2'] - df['high']) / point_size
    df['Bearish_FVG'] = bearish_fvg_cond & (bearish_size >= min_fvg_pips)

    df.drop(['high_shift_2', 'low_shift_2'], axis=1, inplace=True)
    return df

def detect_mss(df: pd.DataFrame, lookback: int = 5) -> pd.DataFrame:
    """
    Detects Market Structure Shift (MSS).
    Requires a previous swing low/high to be broken with momentum.
    """
    if df.empty:
        return df
        
    df = calculate_swing_highs_lows(df, lookback)
    
    # Forward fill the last swing high and low values
    df['Last_Swing_High'] = df['high'].where(df['Swing_High']).ffill()
    df['Last_Swing_Low'] = df['low'].where(df['Swing_Low']).ffill()

    # Bullish MSS: close > Last Swing High
    df['Bullish_MSS'] = (df['close'] > df['Last_Swing_High']) & (df['close'].shift(1) <= df['Last_Swing_High'].shift(1))
    # Bearish MSS: close < Last Swing Low
    df['Bearish_MSS'] = (df['close'] < df['Last_Swing_Low']) & (df['close'].shift(1) >= df['Last_Swing_Low'].shift(1))
    
    return df

def find_order_blocks(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifies Order Blocks (OB).
    Bullish OB: The last down candle before an explosive up move (e.g., FVG or MSS).
    Bearish OB: The last up candle before an explosive down move.
    """
    if df.empty:
        return df
        
    df = detect_fvg(df)
    
    df['Bearish_Candle'] = df['close'] < df['open']
    df['Bullish_Candle'] = df['close'] > df['open']
    
    # Advanced logic requires keeping state of active unmitigated OBs
    # This acts as a foundation.
    return df
