import sys
import os
import datetime
import pandas as pd
import numpy as np

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
        print(f"Fetching {tick_count} ticks for {symbol}...")
        ticks = gateway.get_ticks(symbol, datetime.datetime.now(), tick_count)
        
        if ticks is None or len(ticks) == 0:
            print("ERROR: No tick data retrieved.")
            return

        # 2. Process Data & Engineer Features
        print("Transforming raw ticks into micro-structure features...")
        df = pd.DataFrame(ticks)
        df['time_ms'] = df['time_msc']
        df['mid'] = (df['bid'] + df['ask']) / 2
        
        # Calculate features (simplified for bulk processing)
        df['spread'] = df['ask'] - df['bid']
        df['vol_imbalance'] = df['bid_volume'] - df['ask_volume']
        for n in [10, 50, 100]:
            df[f'momentum_{n}'] = df['mid'].diff(n)
        
        # Velocity calculation (optimized for bulk)
        df['velocity'] = pd.to_datetime(df['time_ms'], unit='ms').to_series().rolling('500ms').count().values
        
        # 3. Label Events (Triple-Barrier Method)
        print("Labeling alpha events using Triple-Barrier Method...")
        df = labeler.label_data(df)
        df = df.dropna()
        
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
 Riverside, CA
