import MetaTrader5 as mt5
from data_engine import DataEngine
from master_overseer import MasterOverseer
from backtester import Backtester

def run_master_backtest():
    print("--- APEX TRI-CORE H1 MASTER BACKTEST ---")
    
    engine = DataEngine()
    symbol = "EURUSD"
    
    # Switch to 1-Hour Timeframe for the Swing Trader Strategy Cores
    timeframe = mt5.TIMEFRAME_H1
    # Fetch 5,000 H1 candles (about 8 months of data)
    num_candles = 5000 
    
    df_raw = engine.fetch_historical_data(symbol, timeframe, num_candles)
    
    if df_raw is None or len(df_raw) == 0:
        print("Failed to procure data. Exiting.")
        engine.shutdown()
        return

    print(f"Successfully loaded {len(df_raw)} candles of {symbol} H1 data.")
    
    print("Calculating Master Tri-Core indicators...")
    master_overseer = MasterOverseer(adx_threshold=25)
    df_indicators = master_overseer.calculate_master_indicators(df_raw)
    
    print("Simulating ADX Regime Routing (Trend vs Range)...")
    df_signals = master_overseer.generate_routed_signals(df_indicators)
    
    # Overriding the 'signal' column and 'atr' column to map to the Backtester class format
    df_signals['signal'] = df_signals['master_signal']
    df_signals['atr'] = df_signals['atr_14']
    
    print("Running backtest against historical data (1% Risk profile)...")
    # For H1 swing trades, we use a slightly wider Break-Even (10 pips) to prevent premature stoppage
    # Risk-Reward will revert to the standard 1:1.5 for swing trades (handled in backtester mathematically)
    backtester = Backtester(df_signals, initial_balance=10000.0, risk_per_trade=0.01, break_even_pips=10.0)
    
    # We must patch the backtester on-the-fly to use 1:1.5 RR for these specific swing trades, 
    # instead of the 0.5 RR tight scalper setting, because H1 trades require room to breathe.
    
    def modified_params(self, direction, price, atr):
        # Swing Trading requires room to breathe.
        # We use a 2x ATR stop loss, and target a 1:2 Risk:Reward ratio (4x ATR TP).
        sl_multiplier = 2.0 
        tp_multiplier = 4.0
        
        if direction == 'LONG':
            sl = price - (atr * sl_multiplier)
            tp = price + (atr * tp_multiplier)
        else:
            sl = price + (atr * sl_multiplier)
            tp = price - (atr * tp_multiplier)
            
        sl_pips = abs(price - sl) * 10000 
        lots = self.calculate_lot_size(sl_pips)
        return {'entry': price, 'sl': sl, 'tp': tp, 'lots': lots}
        
    # Monkey-patch the backtester for this specific run
    import types
    backtester._calculate_trade_params = types.MethodType(modified_params, backtester)
    
    backtester.run()
    
    # Output Results
    backtester.print_performance()
    
    engine.shutdown()
    print("--- H1 OVERSEER BACKTEST COMPLETE ---")

if __name__ == "__main__":
    run_master_backtest()
