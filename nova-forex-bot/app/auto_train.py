import sys
import os
import datetime
import pandas as pd
import numpy as np
import MetaTrader5 as mt5

# Add root directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.mt5_gateway import MT5Gateway
from core.data_engine import DataEngine
from core.labeler import TripleBarrierLabeler
from core.model_manager import ModelManager

def run_autopilot_training(tick_count=300000):
    print(f"--- Nova HFT Autopilot: Starting GLOBAL Multi-Symbol Training ---")
    
    gateway = MT5Gateway()
    engine = DataEngine()
    labeler = TripleBarrierLabeler()
    brain = ModelManager()
    
    import json
    with open('config.json', 'r') as f:
        config = json.load(f)
    SYMBOLS = config['trading']['symbols']
    
    if not gateway.connect():
        print("ERROR: Could not connect to MT5. Check your config.json.")
        return

    all_data = []

    try:
        for symbol in SYMBOLS:
            print(f"\n[Asset: {symbol}] Fetching historical ticks...")
            fetch_from = gateway.get_server_time(symbol) - datetime.timedelta(days=14)
            ticks = gateway.get_ticks_from(symbol, fetch_from, tick_count)
            
            if ticks is None or len(ticks) == 0:
                print(f"WARNING: No data for {symbol}. Skipping.")
                continue

            # Process Data & Engineer Features
            df = pd.DataFrame(ticks)
            df['time_ms'] = df['time_msc']
            df['mid'] = (df['bid'] + df['ask']) / 2
            
            # Calculate features
            df['spread'] = df['ask'] - df['bid']
            for n in [10, 50, 100]:
                df[f'momentum_{n}'] = df['mid'].diff(n)

            # Micro-RSI
            delta = df['mid'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=50).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=50).mean()
            rs = gain / loss
            df['rsi_50'] = 100 - (100 / (1 + rs))
            df['rsi_50'] = df['rsi_50'].fillna(50)

            # Micro-Bollinger Z-Score
            roll_mean = df['mid'].rolling(window=50).mean()
            roll_std = df['mid'].rolling(window=50).std()
            df['bb_zscore'] = (df['mid'] - roll_mean) / roll_std
            df['bb_zscore'] = df['bb_zscore'].replace([np.inf, -np.inf], np.nan).fillna(0)
            
            # Volatility (Instituional-grade StdDev)
            df['volatility'] = df['mid'].rolling(window=100).std()
            
            # Velocity
            df['time_dt'] = pd.to_datetime(df['time_ms'], unit='ms')
            df['velocity'] = df.rolling('500ms', on='time_dt').count()['mid'].values
            
            # Label events with Dynamic Barriers
            print(f"Labeling {symbol} events with Dynamic Volatility Barriers...")
            df = labeler.label_data(df)
            df = df.dropna()
            
            print(f"Collected {len(df)} samples from {symbol}.")
            all_data.append(df)

        if not all_data:
            print("ERROR: No data collected from any symbol.")
            return

        # Aggregate Global Knowledge
        print("\n--- Aggregating Global Knowledge Ledger ---")
        global_df = pd.concat(all_data, ignore_index=True)
        print(f"Total Traing Samples: {len(global_df)}")
        print(f"Positive Alpha Events: {len(global_df[global_df['target'] == 1])}")

        # Train the Brain
        print("Training Global Dual-Ensemble (XGBoost + Random Forest)...")
        brain.train(global_df)
        
    except Exception as e:
        print(f"AUTOPILOT ERROR: {str(e)}")
    finally:
        gateway.shutdown()
        print("--- Global Training Pipeline Finished ---")

if __name__ == "__main__":
    run_autopilot_training()
