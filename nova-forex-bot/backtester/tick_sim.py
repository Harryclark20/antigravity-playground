import pandas as pd
import numpy as np

class TickBacktester:
    def __init__(self, tp_pips=2.0, sl_pips=1.5, slippage_pips=0.2):
        self.tp_pips = tp_pips
        self.sl_pips = sl_pips
        self.slippage_pips = slippage_pips

    def run_simulation(self, df, model_manager):
        """
        Steps through historical tick data and simulates the HFT AI decisions.
        """
        balance = 10000.0
        trades = []
        in_position = False
        
        print("Starting Tick-by-Tick Simulation...")
        
        for i in range(100, len(df) - 1):
            if in_position:
                # Check for exit (simulation happens on every tick)
                current_tick = df.iloc[i]
                if current_tick['mid'] >= tp_price or current_tick['mid'] <= sl_price:
                    pnl = (current_tick['mid'] - entry_price) if side == 'buy' else (entry_price - current_tick['mid'])
                    pnl_pips = pnl / 0.0001
                    balance += (pnl_pips * 1.0) # Simplified $1 per pip/lot
                    trades.append({"exit_time": current_tick['time_ms'], "pnl": pnl_pips})
                    in_position = False
                continue

            # Check AI Prediction
            # In live, we only take the recent features
            features = df.iloc[i:i+1][['velocity', 'spread', 'momentum_10', 'momentum_50', 'momentum_100', 'vol_imbalance']]
            prob = model_manager.predict_probability(features)
            
            if prob > 0.75: # Prediction Threshold
                side = 'buy'
                entry_tick = df.iloc[i]
                # Include Spread + Slippage penalty
                entry_price = entry_tick['ask'] + (self.slippage_pips * 0.0001)
                tp_price = entry_price + (self.tp_pips * 0.0001)
                sl_price = entry_price - (self.sl_pips * 0.0001)
                in_position = True
        
        print(f"Simulation Finished. Final Balance: {balance}")
        return trades
