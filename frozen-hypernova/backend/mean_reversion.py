import pandas as pd
import numpy as np
import ta

class MeanReversionStrategy:
    def __init__(self):
        """
        Initializes the Mean Reversion ("Rubber Band") strategy.
        Designed to buy the "floor" and sell the "ceiling" of a ranging market.
        """
        self.bb_window = 20
        self.bb_dev = 2.0
        self.rsi_window = 14

    def calculate_indicators(self, df):
        if df is None or len(df) == 0:
            return df
            
        df = df.copy()
        
        # 1. Bollinger Bands (The Floor and Ceiling)
        bb_indicator = ta.volatility.BollingerBands(close=df['close'], window=self.bb_window, window_dev=self.bb_dev)
        df['bb_upper'] = bb_indicator.bollinger_hband()
        df['bb_lower'] = bb_indicator.bollinger_lband()
        df['bb_mid'] = bb_indicator.bollinger_mavg()
        
        # 2. RSI (Momentum Confirmation)
        df['rsi'] = ta.momentum.RSIIndicator(close=df['close'], window=self.rsi_window).rsi()
        
        # 3. Volatility (ATR for Stops)
        df['atr_14'] = ta.volatility.AverageTrueRange(high=df['high'], low=df['low'], close=df['close'], window=14).average_true_range()
        
        # Drop initial NaN rows created by the lookback windows
        df.dropna(inplace=True)
        return df

    def generate_signals(self, df):
        """
        Scans for Mean Reversion setups.
        The "Master Overseer" (ADX < 25) must activate this logic externally.
        """
        df = df.copy()
        df['signal'] = 0
        df['strategy_used'] = 'None'
        
        for i in range(1, len(df)):
             curr = df.iloc[i]
             prev = df.iloc[i-1]
             
             # --- BUY: THE RUBBER BAND SNAPS UP ---
             # Rule: Price pierces the lower Bollinger band floor, and RSI is heavily oversold but hooking up.
             if curr['low'] <= curr['bb_lower']:
                  if prev['rsi'] < 30 and curr['rsi'] > prev['rsi']:
                       df.iloc[i, df.columns.get_loc('signal')] = 1 # BUY
                       df.iloc[i, df.columns.get_loc('strategy_used')] = 'MeanReversion_Buy'
                       
             # --- SELL: THE RUBBER BAND SNAPS DOWN ---
             # Rule: Price pierces the upper Bollinger band ceiling, and RSI is overbought but hooking down.
             elif curr['high'] >= curr['bb_upper']:
                  if prev['rsi'] > 70 and curr['rsi'] < prev['rsi']:
                       df.iloc[i, df.columns.get_loc('signal')] = -1 # SELL
                       df.iloc[i, df.columns.get_loc('strategy_used')] = 'MeanReversion_Sell'

        return df
