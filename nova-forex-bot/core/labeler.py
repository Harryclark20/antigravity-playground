import pandas as pd
import numpy as np

class TripleBarrierLabeler:
    def __init__(self, tp_pips=2.0, sl_pips=1.5, timeout_secs=60):
        self.tp_pips = tp_pips
        self.sl_pips = sl_pips
        self.timeout_secs = timeout_secs

    def label_data(self, df):
        """
        Labels a dataframe of ticks using the Triple-Barrier Method.
        1: Profit hit first
        0: Stop loss or timeout hit first
        """
        labels = []
        for i in range(len(df) - 100): # Ensure we have enough data forward to check barriers
            start_price = df.iloc[i]['mid']
            start_time = df.iloc[i]['time_ms']
            
            # Convert pips to absolute price delta (assumes 5-digit broker)
            tp_delta = self.tp_pips * 0.0001
            sl_delta = self.sl_pips * 0.0001
            
            upper_barrier = start_price + tp_delta
            lower_barrier = start_price - sl_delta
            
            label = 0 # Default (Loss or Timeout)
            
            # Check future ticks
            future_ticks = df.iloc[i+1 : i+500] # Look ahead 500 ticks
            for _, tick in future_ticks.iterrows():
                # Time constraint (Vertical Barrier)
                if (tick['time_ms'] - start_time) > (self.timeout_secs * 1000):
                    break
                
                # Profit Barrier
                if tick['mid'] >= upper_barrier:
                    label = 1
                    break
                
                # Loss Barrier
                if tick['mid'] <= lower_barrier:
                    label = 0
                    break
            
            labels.append(label)
        
        # Pad the labels to match the dataframe length
        labels.extend([np.nan] * (len(df) - len(labels)))
        df['target'] = labels
        return df
