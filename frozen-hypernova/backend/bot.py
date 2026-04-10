import MetaTrader5 as mt5
from data_engine import DataEngine
from indicators import calculate_indicators
from strategy import Strategy
from backtester import Backtester
import sys

# Fix the typo in the import
try:
    from strategy import Strategy
except ImportError:
    print("Error importing Strategy. Ensure strategy.py exists.")
    sys.exit(1)


def run_backtest():
    print("--- APEX HYBRID TRADING BOT INITIALIZING ---")
    
    # 1. Initialize Data Engine & Fetch Data
    engine = DataEngine()
    
    symbol = "EURUSD"
    timeframe = mt5.TIMEFRAME_H1 # 1-Hour chart
    num_candles = 5000 # Roughly 1 year of trading data excluding weekends
    
    df_raw = engine.fetch_historical_data(symbol, timeframe, num_candles)
    
    if df_raw is None or len(df_raw) == 0:
        print("Failed to procure data. Exiting.")
        engine.shutdown()
        return

    print(f"Successfully loaded {len(df_raw)} candles of {symbol} data.")
    
    # 2. Calculate Technical Indicators
    print("Calculating technical indicators...")
    df_indicators = calculate_indicators(df_raw)
    
    # 3. Generate Trading Signals based on Regime Filter
    print("Simulating market regimes and generating trading signals...")
    # Set ADX threshold to 25 to delineate Trend vs Range
    strategy_engine = Strategy(adx_threshold=25) 
    df_signals = strategy_engine.generate_signals(df_indicators)
    
    # 4. Run the Backtest with dynamic Risk Management
    print("Running backtest against historical data (1% Risk profile)...")
    # Start with a $10,000 account, risking 1% per trade
    backtester = Backtester(df_signals, initial_balance=10000.0, risk_per_trade=0.01)
    backtester.run()
    
    # 5. Output Results
    backtester.print_performance()
    
    engine.shutdown()
    print("--- BACKTEST COMPLETE ---")

if __name__ == "__main__":
    run_backtest()
