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

        FEATURE_COLS = ['velocity', 'spread', 'momentum_10', 'momentum_50', 'momentum_100']

        print("Starting Tick-by-Tick Simulation...")

        for i in range(100, len(df) - 1):
            current_tick = df.iloc[i]

            if in_position:
                # Check exit barriers on every tick
                if current_tick['mid'] >= tp_price or current_tick['mid'] <= sl_price:
                    pnl = (current_tick['mid'] - entry_price) if side == 'buy' \
                          else (entry_price - current_tick['mid'])
                    pnl_pips = pnl / 0.0001
                    balance += (pnl_pips * 1.0)  # $1 per pip on micro lot
                    trades.append({
                        "exit_time": current_tick['time_ms'],
                        "pnl": pnl_pips
                    })
                    in_position = False
                continue

            # Get feature slice — only the columns the model was trained on
            features = df.iloc[i:i+1][FEATURE_COLS]
            prob = model_manager.predict_probability(features)

            if prob > 0.75:  # Simulation-level threshold (lower than live for coverage)
                side = 'buy'
                # Include spread + slippage as friction cost
                entry_price = current_tick['ask'] + (self.slippage_pips * 0.0001)
                tp_price = entry_price + (self.tp_pips * 0.0001)
                sl_price = entry_price - (self.sl_pips * 0.0001)
                in_position = True

        print(f"Simulation Finished. Final Balance: ${balance:,.2f} (Started: $10,000.00)")
        return trades
