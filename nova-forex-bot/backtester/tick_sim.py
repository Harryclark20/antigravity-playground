import pandas as pd
import numpy as np

class TickBacktester:
    def __init__(self, tp_pips=2.0, sl_pips=1.5, slippage_pips=0.2):
        self.tp_pips = tp_pips
        self.sl_pips = sl_pips
        self.slippage_pips = slippage_pips

    def run_simulation(self, df, model_manager):
        """
        Steps through historical tick data and simulates HFT AI decisions.
        Applies spread + slippage friction for high-fidelity results.
        """
        balance = 10000.0
        trades = []
        in_position = False
        entry_price = 0.0
        tp_price = 0.0
        sl_price = 0.0
        side = 'buy'

        FEATURE_COLS = ['velocity', 'spread', 'momentum_10', 'momentum_50', 'momentum_100', 'rsi_50', 'bb_zscore']
        
        # Pre-extract numpy data for speed
        feature_matrix = df[FEATURE_COLS].values
        mid_prices = df['mid'].values
        ask_prices = df['ask'].values
        time_ms = df['time_ms'].values

        print("Starting Optimized Tick-by-Tick Simulation...")

        for i in range(len(df) - 1):
            current_mid = mid_prices[i]

            if in_position:
                # Check exit barriers on every tick
                if (side == 'buy' and current_mid >= tp_price) or \
                   (side == 'buy' and current_mid <= sl_price):
                    
                    pnl = (current_mid - entry_price) if side == 'buy' \
                          else (entry_price - current_mid)
                    pnl_pips = pnl / 0.0001
                    balance += (pnl_pips * 1.0)
                    trades.append({
                        "exit_time": time_ms[i],
                        "pnl": pnl_pips
                    })
                    in_position = False
                continue

            # Vectorized feature access
            features = feature_matrix[i].reshape(1, -1)
            prob = model_manager.predict_probability(pd.DataFrame(features, columns=FEATURE_COLS))

            if prob > 0.75:  # Matched to NEW production threshold (75% Dual Model agreement)
                side = 'buy'
                entry_price = ask_prices[i] + (self.slippage_pips * 0.0001)
                tp_price = entry_price + (self.tp_pips * 0.0001)
                sl_price = entry_price - (self.sl_pips * 0.0001)
                in_position = True

        print(f"Simulation Finished. Final Balance: ${balance:,.2f} (Started: $10,000.00)")
        return trades
