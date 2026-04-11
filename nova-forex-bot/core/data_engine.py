import pandas as pd
import numpy as np

class DataEngine:
    def __init__(self, velocity_window_ms=500):
        self.velocity_window_ms = velocity_window_ms

    def engineer_features(self, ticks):
        """
        Transforms raw ticks into micro-structure features.
        Expects a numpy array of ticks from mt5.copy_ticks_from.
        """
        if ticks is None or len(ticks) == 0:
            return None
        
        df = pd.DataFrame(ticks)
        df['time_ms'] = df['time_msc'] # Use millisecond timestamps
        
        # 1. Spread Imbalance
        df['spread'] = df['ask'] - df['bid']
        
        # 2. Tick Velocity (Ticks per rolling 500ms)
        # We calculate how many ticks occurred in the last self.velocity_window_ms
        df['velocity'] = df['time_ms'].rolling(window='500ms', on=pd.to_datetime(df['time_ms'], unit='ms')).count()

        # 3. Micro-Momentum (Rate of change over 10, 50, 100 ticks)
        # We look at the weighted average price (mid price)
        df['mid'] = (df['bid'] + df['ask']) / 2
        
        for n in [10, 50, 100]:
            df[f'momentum_{n}'] = df['mid'].diff(n)
            
        # 4. Bid/Ask Volume Imbalance (if volume is available)
        # Note: In MetaTrader 5, 'volume' in ticks depends on the broker/symbol
        df['vol_imbalance'] = df['bid_volume'] - df['ask_volume']

        # Cleanup: Remove NaN values produced by momentum diffs
        features = df.dropna().tail(1) # Return the most recent processed tick as a feature vector
        
        return features
