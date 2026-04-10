import pandas as pd
import numpy as np
import ta

class SniperStrategy:
    def __init__(self):
        """
        Initializes the High-Probability Scalping Strategy.
        Designed for M1 or M5 timeframes with aggressive risk management.
        """
        self.fast_ema_len = 9
        self.slow_ema_len = 21
        self.rsi_len = 7

    def calculate_snip_indicators(self, df):
        """Calculates indicators specifically for the Sniper Scalper."""
        if df is None or len(df) == 0:
            return df
            
        df = df.copy()
        
        # 1. Micro-Trend Identification (Fast EMAs)
        df['ema_9'] = ta.trend.ema_indicator(close=df['close'], window=self.fast_ema_len)
        df['ema_21'] = ta.trend.ema_indicator(close=df['close'], window=self.slow_ema_len)
        
        # 2. Pullback Identification (Fast RSI)
        df['rsi_7'] = ta.momentum.RSIIndicator(close=df['close'], window=self.rsi_len).rsi()
        
        # 3. Micro-Volatility (Fast ATR for tight stops)
        df['atr_5'] = ta.volatility.AverageTrueRange(high=df['high'], low=df['low'], close=df['close'], window=5).average_true_range()
        
        df.dropna(inplace=True)
        return df

    def generate_signals(self, df):
        """
        Scans for high-probability pullback continuation setups.
        """
        df = df.copy()
        df['signal'] = 0
        df['strategy_used'] = 'None'
        
        for i in range(1, len(df)):
            curr = df.iloc[i]
            prev = df.iloc[i-1]
            
            # --- UPTREND SCALPING ---
            if curr['ema_9'] > curr['ema_21']:
                # The "Pullback" condition: Price dipped, RSI cooled off, but trend holds
                if prev['rsi_7'] < 40 and curr['rsi_7'] > prev['rsi_7'] and curr['close'] > curr['ema_9']:
                     df.iloc[i, df.columns.get_loc('signal')] = 1 # BUY
                     df.iloc[i, df.columns.get_loc('strategy_used')] = 'Sniper_Buy'

            # --- DOWNTREND SCALPING ---
            elif curr['ema_9'] < curr['ema_21']:
                 # The "Pullback" condition: Price rallied, RSI became overbought, trend holds
                 if prev['rsi_7'] > 60 and curr['rsi_7'] < prev['rsi_7'] and curr['close'] < curr['ema_9']:
                      df.iloc[i, df.columns.get_loc('signal')] = -1 # SELL
                      df.iloc[i, df.columns.get_loc('strategy_used')] = 'Sniper_Sell'

        return df
