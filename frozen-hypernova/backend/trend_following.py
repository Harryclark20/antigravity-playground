import pandas as pd
import numpy as np
import ta

class TrendFollowingStrategy:
    def __init__(self):
        """
        Initializes the Trend Following ("Home Run") strategy.
        Designed to capture massive swings when a true macroeconomic trend breaks out.
        """
        self.fast_ema = 50
        self.slow_ema = 200

    def calculate_indicators(self, df):
        if df is None or len(df) == 0:
            return df
            
        df = df.copy()
        
        # 1. Macro-Trend Identification (EMAs)
        df['ema_50'] = ta.trend.ema_indicator(close=df['close'], window=self.fast_ema)
        df['ema_200'] = ta.trend.ema_indicator(close=df['close'], window=self.slow_ema)
        
        # 2. Entry Trigger (MACD)
        macd_indicator = ta.trend.MACD(close=df['close'], window_slow=26, window_fast=12, window_sign=9)
        df['macd_line'] = macd_indicator.macd()
        df['macd_signal'] = macd_indicator.macd_signal()
        df['macd_hist'] = macd_indicator.macd_diff()
        
        # 3. Volatility (ATR for wide trailing stops)
        df['atr_14'] = ta.volatility.AverageTrueRange(high=df['high'], low=df['low'], close=df['close'], window=14).average_true_range()
        
        df.dropna(inplace=True)
        return df

    def generate_signals(self, df):
        """
        Scans for major Trend breakout entries.
        The "Master Overseer" (ADX > 25) must activate this logic externally.
        """
        df = df.copy()
        df['signal'] = 0
        df['strategy_used'] = 'None'
        
        for i in range(1, len(df)):
             curr = df.iloc[i]
             prev = df.iloc[i-1]
             
             # --- HUGE UPTREND DETECTED ---
             # Rule: The 50 EMA is above the 200 EMA (Golden Cross State)
             if curr['ema_50'] > curr['ema_200']:
                  # Entry: Wait for the MACD line to cross back ABOVE the Signal line
                  if prev['macd_line'] <= prev['macd_signal'] and curr['macd_line'] > curr['macd_signal']:
                       df.iloc[i, df.columns.get_loc('signal')] = 1 # BUY
                       df.iloc[i, df.columns.get_loc('strategy_used')] = 'Trend_MACD_Buy'
                       
             # --- HUGE DOWNTREND DETECTED ---
             # Rule: The 50 EMA is below the 200 EMA (Death Cross State)
             elif curr['ema_50'] < curr['ema_200']:
                  # Entry: Wait for the MACD line to cross back BELOW the Signal line
                  if prev['macd_line'] >= prev['macd_signal'] and curr['macd_line'] < curr['macd_signal']:
                       df.iloc[i, df.columns.get_loc('signal')] = -1 # SELL
                       df.iloc[i, df.columns.get_loc('strategy_used')] = 'Trend_MACD_Sell'

        return df
