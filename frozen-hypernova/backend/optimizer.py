import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from itertools import product
from data_engine import DataEngine
from indicators import calculate_indicators
from strategy import Strategy
from backtester import Backtester
import warnings

# Suppress pandas FutureWarnings from ta library
warnings.simplefilter(action='ignore', category=FutureWarning)

def optimize_strategy():
    print("--- APEX HYBRID GRID SEARCH OPTIMIZER ---")
    
    # 1. Fetch Static Data Once
    engine = DataEngine()
    symbol = "EURUSD"
    timeframe = mt5.TIMEFRAME_H1
    num_candles = 5000
    df_raw = engine.fetch_historical_data(symbol, timeframe, num_candles)
    
    if df_raw is None or len(df_raw) == 0:
        print("Failed to procure data.")
        engine.shutdown()
        return
        
    engine.shutdown()

    # Define the parameter grid to search through
    # For a real optimizer, we would re-calculate indicators here if we were changing lengths (e.g., EMA windows)
    # To save time, we will optimize the Strategy constraints (ADX Thresholds) and Risk Multipliers
    
    # Calculate base indicators once
    print("Calculating base indicators...")
    df_indicators = calculate_indicators(df_raw)

    # Grid search parameters
    adx_thresholds = [20, 25, 30, 35]
    risk_per_trade = [0.01] # Keep fixed at 1% for fair comparison
    
    best_profit_factor = 0
    best_params = {}
    results = []

    print(f"Running grid search over {len(adx_thresholds)} combinations...")
    
    for adx in adx_thresholds:
        # Generate signals based on current parameter
        strategy_engine = Strategy(adx_threshold=adx)
        df_signals = strategy_engine.generate_signals(df_indicators)
        
        # Run Backtest
        backtester = Backtester(df_signals, initial_balance=10000.0, risk_per_trade=0.01)
        # Suppress prints from backtester to avoid console spam
        backtester.run()
        
        # Calculate bare metrics manually to bypass print_performance()
        trades_df = pd.DataFrame(backtester.trades)
        if len(trades_df) > 0:
            gross_profit = trades_df[trades_df['PnL'] > 0]['PnL'].sum()
            gross_loss = abs(trades_df[trades_df['PnL'] <= 0]['PnL'].sum())
            pf = gross_profit / gross_loss if gross_loss > 0 else 0
            win_rate = (len(trades_df[trades_df['PnL'] > 0]) / len(trades_df)) * 100
            
            results.append({
                'ADX Threshold': adx,
                'Total Trades': len(trades_df),
                'Win Rate %': round(win_rate, 2),
                'Profit Factor': round(pf, 2),
                'Net Profit $': round(backtester.equity - 10000.0, 2)
            })
            
            if pf > best_profit_factor:
                 best_profit_factor = pf
                 best_params = {'ADX Option': adx, 'PF Option': pf}

    print("\n--- OPTIMIZATION RESULTS ---")
    results_df = pd.DataFrame(results).sort_values(by='Profit Factor', ascending=False)
    print(results_df.to_string(index=False))
    
    if best_profit_factor > 1.0:
        print(f"\nFOUND PROFITABLE PARAMETERS: ADX > {best_params['ADX Option']} yielded a Profit Factor of {best_params['PF Option']:.2f}")
    else:
        print("\nGrid search failed to find a highly profitable combination. Strategy logic pivot required.")

if __name__ == "__main__":
    optimize_strategy()
