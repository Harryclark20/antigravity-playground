import sys
import os
import datetime
import pandas as pd

# Add root directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.mt5_gateway import MT5Gateway
from core.data_engine import DataEngine
from core.model_manager import ModelManager
from backtester.tick_sim import TickBacktester

def run_autopilot_validation(symbol="EURUSD", test_ticks=100000):
    print(f"--- Nova HFT Autopilot: Starting Validation Engine for {symbol} ---")
    
    gateway = MT5Gateway()
    brain = ModelManager()
    sim = TickBacktester()
    
    if not gateway.connect():
        print("ERROR: Connection failed.")
        return

    try:
        # 1. Fetch Fresh Testing Data
        # We fetch data ending NOW to see how the model performs on the absolute latest price action
        print(f"Fetching {test_ticks} validation ticks...")
        ticks = gateway.get_ticks(symbol, datetime.datetime.now(), test_ticks)
        
        if ticks is None:
            print("ERROR: No data for validation.")
            return
            
        df = pd.DataFrame(ticks)
        df['time_ms'] = df['time_msc']
        df['mid'] = (df['bid'] + df['ask']) / 2
        df['spread'] = df['ask'] - df['bid']
        df['vol_imbalance'] = df['bid_volume'] - df['ask_volume']
        for n in [10, 50, 100]:
            df[f'momentum_{n}'] = df['mid'].diff(n)
        df['velocity'] = pd.to_datetime(df['time_ms'], unit='ms').to_series().rolling('500ms').count().values
        df = df.dropna()

        # 2. Run High-Fidelity Simulator
        print("Running Event-Driven Simulation with Spread/Slippage Friction...")
        trades = sim.run_simulation(df, brain)
        
        # 3. Generate Performance Report
        if len(trades) > 0:
            trades_df = pd.DataFrame(trades)
            win_rate = (len(trades_df[trades_df['pnl'] > 0]) / len(trades_df)) * 100
            total_pnl = trades_df['pnl'].sum()
            
            print("\n" + "="*40)
            print("       NOVA HFT PERFORMANCE REPORT")
            print("="*40)
            print(f"Total Trades:    {len(trades_df)}")
            print(f"Win Rate:        {win_rate:.2f}%")
            print(f"Total Pips:      {total_pnl:.2f}")
            print(f"Avg Pnl/Trade:   {(total_pnl/len(trades_df)):.2f} pips")
            print("="*40)
        else:
            print("No trades triggered during the validation period.")

    finally:
        gateway.shutdown()
        print("--- Validation Engine Finished ---")

if __name__ == "__main__":
    run_autopilot_validation()
 Riverside, CA
