import MetaTrader5 as mt5
from data_engine import DataEngine
from sniper import SniperStrategy
from backtester import Backtester

def run_sniper_backtest():
    print("--- APEX SNIPER SCALPER INITIALIZING ---")
    
    engine = DataEngine()
    symbol = "EURUSD"
    
    # Switch to 5-Minute Timeframe for scalping
    timeframe = mt5.TIMEFRAME_M5 
    # Fetch 10,000 M5 candles (about 1 month of trading data)
    num_candles = 10000 
    
    df_raw = engine.fetch_historical_data(symbol, timeframe, num_candles)
    
    if df_raw is None or len(df_raw) == 0:
        print("Failed to procure data. Exiting.")
        engine.shutdown()
        return

    print(f"Successfully loaded {len(df_raw)} candles of {symbol} M5 data.")
    
    # 2. Calculate Sniper Technical Indicators
    print("Calculating scalping indicators...")
    strategy_engine = SniperStrategy()
    df_indicators = strategy_engine.calculate_snip_indicators(df_raw)
    
    # 3. Generate Signals
    print("Simulating micro-market pullbacks...")
    df_signals = strategy_engine.generate_signals(df_indicators)
    
    # IMPORTANT: The Sniper Scalper requires an overridden ATR column name to match the backtester expectations
    # The current backtester looks for 'atr', but sniper uses 'atr_5'
    df_signals['atr'] = df_signals['atr_5']
    
    # 4. Run Backtest
    print("Running backtest against historical data (1% Risk, 1:1.5 RR profile)...")
    # For true Sniper capabilities, the backtester would need Break-Even enforcement logic.
    # We run the baseline M5 strategy first to test the raw win rate of the new pull-back indicator logic.
    backtester = Backtester(df_signals, initial_balance=10000.0, risk_per_trade=0.01)
    backtester.run()
    
    # 5. Output Results
    backtester.print_performance()
    
    engine.shutdown()
    print("--- SNIPER BACKTEST COMPLETE ---")

if __name__ == "__main__":
    run_sniper_backtest()
