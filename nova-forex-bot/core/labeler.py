import pandas as pd
import numpy as np

class TripleBarrierLabeler:
    def __init__(self, tp_pips=2.0, sl_pips=1.5, timeout_secs=60):
        self.tp_pips = tp_pips
        self.sl_pips = sl_pips
        self.timeout_secs = timeout_secs

    def label_data(self, df):
        """
        Labels a dataframe of ticks using Volatility-Adjusted Triple-Barrier.
        1: Profit hit first
        0: Stop loss or timeout hit first
        """
        labels = np.zeros(len(df))
        labels[:] = np.nan
        
        mids = df['mid'].values
        times = df['time_ms'].values
        vols = df['volatility'].values
        
        timeout_ms = self.timeout_secs * 1000
        
        for i in range(len(df) - 100):
            start_price = mids[i]
            start_time = times[i]
            current_vol = vols[i]
            
            # Skip if volatility is not available yet
            if np.isnan(current_vol) or current_vol == 0:
                continue

            # Dynamic Barriers: Institutional multiples of Standard Deviation
            # Typically HFT uses 2-3x Volatility for targets
            upper_barrier = start_price + (current_vol * 3.0)
            lower_barrier = start_price - (current_vol * 2.0)
            
            label = 0 # Default (Loss or Timeout)
            
            # Look ahead up to 500 ticks
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
