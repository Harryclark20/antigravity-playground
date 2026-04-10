import pandas as pd
import numpy as np

class Strategy:
    def __init__(self, adx_threshold=25):
        """
        Initializes the Hybrid Trading Strategy.
        
        Args:
            adx_threshold (int): The ADX value that delineates a trending market 
                                 from a ranging market. Usually 20 or 25.
        """
        self.adx_threshold = adx_threshold

    def generate_signals(self, df):
        """
        Scans the DataFrame and generates BUY (1), SELL (-1), or HOLD (0) signals.
        
        Args:
            df (pd.DataFrame): DataFrame with calculated technical indicators.
            
        Returns:
            pd.DataFrame: Original DataFrame with a new 'signal' column.
        """
        df = df.copy()
        
        # Initialize signal column with 0 (HOLD)
        df['signal'] = 0
        df['strategy_used'] = 'None'
        
        # Iterate through the DataFrame (we need previous rows for crossover logic)
        for i in range(1, len(df)):
            curr = df.iloc[i]
            prev = df.iloc[i-1]
            
            # --- OVERSEER: REGIME DETECTION ---
            is_trending = curr['adx'] > self.adx_threshold
            
            # --- STRATEGY A: TREND FOLLOWING (Momentum) ---
            if is_trending:
                # Up Trend Condition: 50 EMA is above 200 EMA
                if curr['ema_50'] > curr['ema_200']:
                    # Trigger: MACD Line crosses ABOVE Signal Line
                    if prev['macd_line'] <= prev['macd_signal'] and curr['macd_line'] > curr['macd_signal']:
                        df.iloc[i, df.columns.get_loc('signal')] = 1 # BUY
                        df.iloc[i, df.columns.get_loc('strategy_used')] = 'Trend_MACD_Cross_Up'
                        
                # Down Trend Condition: 50 EMA is below 200 EMA
                elif curr['ema_50'] < curr['ema_200']:
                    # Trigger: MACD Line crosses BELOW Signal Line
                    if prev['macd_line'] >= prev['macd_signal'] and curr['macd_line'] < curr['macd_signal']:
                        df.iloc[i, df.columns.get_loc('signal')] = -1 # SELL
                        df.iloc[i, df.columns.get_loc('strategy_used')] = 'Trend_MACD_Cross_Down'


            # --- STRATEGY B: MEAN REVERSION (Range Bound) ---
            else:
                # Buy Condition: Price hits lower BB AND RSI is Oversold (< 30) AND hooking up
                if curr['low'] <= curr['bb_lower']:
                     if prev['rsi'] < 30 and curr['rsi'] > prev['rsi']:
                        df.iloc[i, df.columns.get_loc('signal')] = 1 # BUY
                        df.iloc[i, df.columns.get_loc('strategy_used')] = 'Range_BB_Bounce_Up'
                
                # Sell Condition: Price hits upper BB AND RSI is Overbought (> 70) AND hooking down
                elif curr['high'] >= curr['bb_upper']:
                     if prev['rsi'] > 70 and curr['rsi'] < prev['rsi']:
                        df.iloc[i, df.columns.get_loc('signal')] = -1 # SELL
                        df.iloc[i, df.columns.get_loc('strategy_used')] = 'Range_BB_Bounce_Down'

        return df
