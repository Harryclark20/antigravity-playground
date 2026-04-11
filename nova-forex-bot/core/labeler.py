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
        labels = np.zeros(len(df))
        labels[:] = np.nan
        
        mids = df['mid'].values
        times = df['time_ms'].values
        
        tp_delta = self.tp_pips * 0.0001
        sl_delta = self.sl_pips * 0.0001
        timeout_ms = self.timeout_secs * 1000
        
        for i in range(len(df) - 100):
            start_price = mids[i]
            start_time = times[i]
            
            upper_barrier = start_price + tp_delta
            lower_barrier = start_price - sl_delta
            
            label = 0 # Default (Loss or Timeout)
            
            # Look ahead up to 500 ticks using direct array access
            for j in range(i + 1, min(i + 500, len(df))):
                if (times[j] - start_time) > timeout_ms:
                    break
                if mids[j] >= upper_barrier:
                    label = 1
                    break
                if mids[j] <= lower_barrier:
                    label = 0
                    break
            
            labels[i] = label
        
        df['target'] = labels
        return df
