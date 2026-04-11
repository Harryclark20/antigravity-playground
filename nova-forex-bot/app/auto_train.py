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

def run_autopilot_training(symbol="EURUSD", tick_count=500000):
    print(f"--- Nova HFT Autopilot: Starting Training Pipeline for {symbol} ---")
    
    gateway = MT5Gateway()
    engine = DataEngine()
    labeler = TripleBarrierLabeler()
    brain = ModelManager()
    
    if not gateway.connect():
        print("ERROR: Could not connect to MT5. Check your config.json.")
        return

    try:
        # 1. Fetch Historical Ticks
        # Starting 14 days before broker server time (timezone-safe)
        fetch_from = gateway.get_server_time(symbol) - datetime.timedelta(days=14)
        print(f"Fetching {tick_count} ticks for {symbol} starting from {fetch_from}...")
        
        ticks = gateway.get_ticks_from(symbol, fetch_from, tick_count)
        
        if ticks is None or len(ticks) == 0:
            print("ERROR: No tick data retrieved.")
            return

        # 2. Process Data & Engineer Features
        print("Transforming raw ticks into micro-structure features...")
        df = pd.DataFrame(ticks)
        df['time_ms'] = df['time_msc']
        df['mid'] = (df['bid'] + df['ask']) / 2
        
        print(f"Dataframe initialized: {df.shape}")
        
        # Calculate features (simplified for bulk processing)
        df['spread'] = df['ask'] - df['bid']
        for n in [10, 50, 100]:
            df[f'momentum_{n}'] = df['mid'].diff(n)
        
        # Velocity calculation (optimized for bulk)
        df['time_dt'] = pd.to_datetime(df['time_ms'], unit='ms')
        df['velocity'] = df.rolling('500ms', on='time_dt').count()['mid'].values
        print(f"Features calculated: {df.shape}")
        
        # 3. Label Events (Triple-Barrier Method)
        print("Labeling alpha events using Triple-Barrier Method...")
        df = labeler.label_data(df)
        print(f"Data labeled: {df.shape}")
        
        df = df.dropna()
        print(f"Data after dropna: {df.shape}")
        
        if len(df) > 0:
            print(f"Sample row:\n{df.tail(1)}")
        
        print(f"Processed {len(df)} samples with {len(df[df['target'] == 1])} positive events.")

        # 4. Train the Brain
        print("Training XGBoost Alpha Model...")
        brain.train(df)
        
    except Exception as e:
        print(f"AUTOPILOT ERROR: {str(e)}")
    finally:
        gateway.shutdown()
        print("--- Training Pipeline Finished ---")

if __name__ == "__main__":
    run_autopilot_training()
