import sys
import os
import datetime
import pandas as pd

# Add root directory to path for local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.mt5_gateway import MT5Gateway
from core.model_manager import ModelManager
from backtester.tick_sim import TickBacktester

FEATURE_COLS = ['velocity', 'spread', 'momentum_10', 'momentum_50', 'momentum_100']

def run_autopilot_validation(symbol="EURUSD", test_ticks=100000):
    print(f"--- Nova HFT Autopilot: Starting Validation Engine for {symbol} ---")

    gateway = MT5Gateway()
    brain = ModelManager()
    sim = TickBacktester()

    if not gateway.connect():
        print("ERROR: Connection failed.")
        return

    try:
        # Fetch from 7 days ago (UTC) — MT5 server always operates on UTC
        fetch_from = datetime.datetime.utcnow() - datetime.timedelta(days=7)
        print(f"Fetching {test_ticks} validation ticks from {fetch_from}...")
        ticks = gateway.get_ticks(symbol, fetch_from, test_ticks)

        if ticks is None or len(ticks) == 0:
            print("ERROR: No data for validation.")
            return

        # Build feature dataframe (must match training pipeline exactly)
        df = pd.DataFrame(ticks)
        df['time_ms'] = df['time_msc']
        df['mid'] = (df['bid'] + df['ask']) / 2
        df['spread'] = df['ask'] - df['bid']
        for n in [10, 50, 100]:
            df[f'momentum_{n}'] = df['mid'].diff(n)
        df['time_dt'] = pd.to_datetime(df['time_ms'], unit='ms')
        df = df.sort_values('time_dt').reset_index(drop=True)
        df['velocity'] = df.rolling('500ms', on='time_dt').count()['mid']
        df = df.dropna()

        if len(df) < 200:
            print(f"ERROR: Insufficient data after processing ({len(df)} rows).")
            return

        print(f"Validation dataset: {len(df):,} clean ticks.")

        # Run Simulation
        print("Running Event-Driven Simulation with Spread/Slippage Friction...")
        trades = sim.run_simulation(df, brain)

        # Performance Report
        print("\n" + "="*40)
        print("       NOVA HFT PERFORMANCE REPORT")
        print("="*40)
        if len(trades) > 0:
            trades_df = pd.DataFrame(trades)
            win_count = len(trades_df[trades_df['pnl'] > 0])
            total_trades = len(trades_df)
            win_rate = (win_count / total_trades) * 100
            total_pnl = trades_df['pnl'].sum()
            avg_pnl = total_pnl / total_trades
            max_loss = trades_df['pnl'].min()
            max_win = trades_df['pnl'].max()

            print(f"Total Trades:     {total_trades}")
            print(f"Win Rate:         {win_rate:.2f}%")
            print(f"Total Pips P&L:   {total_pnl:.2f}")
            print(f"Avg Pip/Trade:    {avg_pnl:.2f}")
            print(f"Best Trade:       +{max_win:.2f} pips")
            print(f"Worst Trade:      {max_loss:.2f} pips")
        else:
            print("No trades triggered during the validation period.")
            print("Consider lowering the confidence threshold in tick_sim.py (currently 0.75).")
        print("="*40)

    except Exception as e:
        print(f"VALIDATION ERROR: {e}")
    finally:
        gateway.shutdown()
        print("--- Validation Engine Finished ---")

if __name__ == "__main__":
    run_autopilot_validation()
