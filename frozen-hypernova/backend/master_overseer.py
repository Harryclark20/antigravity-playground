import pandas as pd
import numpy as np
import ta
from mean_reversion import MeanReversionStrategy
from trend_following import TrendFollowingStrategy

class MasterOverseer:
    def __init__(self, adx_threshold=25):
        """
        Initializes the Master Strategy Router.
        Uses ADX to determine if the market is Ranging or Trending.
        """
        self.adx_threshold = adx_threshold
        self.mean_reversion_engine = MeanReversionStrategy()
        self.trend_following_engine = TrendFollowingStrategy()

    def calculate_master_indicators(self, df):
        """
        Calculates the ADX regime filter, and then calls the sub-engines
        to calculate their respective indicators.
        """
        if df is None or len(df) == 0:
            return df
            
        df = df.copy()
        
        # 1. The Regime Filter (ADX)
        adx_indicator = ta.trend.ADXIndicator(high=df['high'], low=df['low'], close=df['close'], window=14)
        df['adx'] = adx_indicator.adx()
        
        # 2. Calculate Sub-Strategy Indicators (Appending to the same DataFrame)
        df = self.mean_reversion_engine.calculate_indicators(df)
        df = self.trend_following_engine.calculate_indicators(df)
        
        df.dropna(inplace=True)
        return df

    def generate_routed_signals(self, df):
        """
        The routing logic. Checks the ADX regime on every row.
        If Trending: Asks the Trend engine for a signal.
        If Ranging: Asks the Mean Reversion engine for a signal.
        """
        df = df.copy()
        df['master_signal'] = 0
        df['master_strategy'] = 'None'
        df['regime'] = 'Unknown'
        
        # Pre-calculate all sub-signals to optimize the loop
        df_mr_signals = self.mean_reversion_engine.generate_signals(df)
        df_tf_signals = self.trend_following_engine.generate_signals(df)
        
        for i in range(1, len(df)):
             curr_adx = df.iloc[i]['adx']
             
             # --- REGIME ROUTING ---
             if curr_adx >= self.adx_threshold:
                  df.iloc[i, df.columns.get_loc('regime')] = 'TRENDING'
                  
                  # Ask Trend engine for action
                  signal = df_tf_signals.iloc[i]['signal']
                  strategy = df_tf_signals.iloc[i]['strategy_used']
                  
                  if signal != 0:
                      df.iloc[i, df.columns.get_loc('master_signal')] = signal
                      df.iloc[i, df.columns.get_loc('master_strategy')] = strategy
                      
             elif curr_adx < self.adx_threshold:
                  df.iloc[i, df.columns.get_loc('regime')] = 'RANGING'
                  
                  # Ask Mean Reversion engine for action
                  signal = df_mr_signals.iloc[i]['signal']
                  strategy = df_mr_signals.iloc[i]['strategy_used']
                  
                  if signal != 0:
                      df.iloc[i, df.columns.get_loc('master_signal')] = signal
                      df.iloc[i, df.columns.get_loc('master_strategy')] = strategy

        return df
