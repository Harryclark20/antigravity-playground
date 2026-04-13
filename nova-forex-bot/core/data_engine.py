import pandas as pd
import numpy as np

class DataEngine:
    def __init__(self, velocity_window_ms=500):
        self.velocity_window_ms = velocity_window_ms

    def engineer_features(self, ticks):
        """
        Transforms raw ticks into micro-structure features.
        Expects a numpy array of ticks from mt5.copy_ticks_from.
        Returns a single-row DataFrame representing the latest processed tick.
        """
        if ticks is None or len(ticks) < 101:
            # Need at least 101 rows: 100 for momentum_100 + 1 for current tick
            return None

        df = pd.DataFrame(ticks)
        df['time_ms'] = df['time_msc']  # Use millisecond timestamps

        # 1. Spread Imbalance (in price, not pips)
        df['spread'] = df['ask'] - df['bid']

        # 2. Mid Price
        df['mid'] = (df['bid'] + df['ask']) / 2

        # 3. Tick Velocity — using time-based rolling window correctly
        df['time_dt'] = pd.to_datetime(df['time_ms'], unit='ms')
        df = df.sort_values('time_dt').reset_index(drop=True)
        df['velocity'] = df.rolling(f'{self.velocity_window_ms}ms', on='time_dt').count()['mid']

        # 4. Micro-Momentum (rate of change over last N ticks)
        for n in [10, 50, 100]:
            df[f'momentum_{n}'] = df['mid'].diff(n)

        # 5. Micro-RSI (50 ticks)
        delta = df['mid'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=50).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=50).mean()
        rs = gain / loss
        df['rsi_50'] = 100 - (100 / (1 + rs))
        df['rsi_50'] = df['rsi_50'].fillna(50)

        # 6. Micro-Bollinger Band Z-Score (50 ticks)
        roll_mean = df['mid'].rolling(window=50).mean()
        roll_std = df['mid'].rolling(window=50).std()
        df['bb_zscore'] = (df['mid'] - roll_mean) / roll_std
        df['bb_zscore'] = df['bb_zscore'].replace([np.inf, -np.inf], np.nan).fillna(0)

        # 7. Tick Volatility (100-tick Std)
        df['volatility'] = df['mid'].rolling(window=100).std()

        # Return only the latest valid (non-NaN) row
        features = df.dropna().tail(1)
        return features if len(features) > 0 else None
