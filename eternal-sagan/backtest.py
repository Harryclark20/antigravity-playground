import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import logging
from strategy import MLHybridStrategy

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def run_backtest(symbol="EURUSD", timeframe=mt5.TIMEFRAME_M15):
    if not mt5.initialize():
        logging.error("Initialize failed")
        return
        
    logging.info("--- Starting Backtester ---")
    
    strategy = MLHybridStrategy(symbol, timeframe)
    
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 15000)
    if rates is None:
        logging.error("Failed to fetch data for backtesting.")
        return
        
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    train_df = df.iloc[:10000].copy()
    train_df = strategy.calculate_features(train_df)
    
    future_close = train_df['close'].shift(-3)
    train_df['Target'] = (future_close > train_df['close']).astype(int)
    train_df.dropna(inplace=True)
    
    extended_features = strategy.features + ['Close_to_EMA50', 'Close_to_EMA200']
    X_train = train_df[extended_features]
    y_train = train_df['Target']
    
    logging.info("Training Model for Backtest...")
    strategy.model.fit(X_train, y_train)
    strategy.is_trained = True
    
    test_df = df.iloc[10000:].copy()
    test_df = strategy.calculate_features(test_df)
    test_df.dropna(inplace=True)
    
    # Account Variables
    initial_balance = 10000.0
    balance = initial_balance
    risk_percent = 1.0
    atr_sl_mult = 1.5
    atr_tp_mult = 3.0
    
    in_trade = False
    trade_type = None
    entry_price = 0.0
    sl = 0.0
    tp = 0.0
    lot_size = 0.0
    
    trades_taken = 0
    winning_trades = 0
    losing_trades = 0
    max_drawdown = 0.0
    peak_balance = initial_balance
    
    logging.info(f"Running simulation on {len(test_df)} out-of-sample candles...")
    
    for i in range(len(test_df)):
        row = test_df.iloc[i]
        close_price = row['close']
        high_price = row['high']
        low_price = row['low']
        
        # Check if in trade and hit SL or TP
        if in_trade:
            hit_tp = False
            hit_sl = False
            
            if trade_type == "BUY":
                if high_price >= tp:
                    hit_tp = True
                    exit_price = tp
                elif low_price <= sl:
                    hit_sl = True
                    exit_price = sl
            elif trade_type == "SELL":
                if low_price <= tp:
                    hit_tp = True
                    exit_price = tp
                elif high_price >= sl:
                    hit_sl = True
                    exit_price = sl
                    
            if hit_tp or hit_sl:
                points_won_lost = (exit_price - entry_price) if trade_type == "BUY" else (entry_price - exit_price)
                
                pnl = points_won_lost * 100000 * lot_size
                balance += pnl
                trades_taken += 1
                
                if pnl > 0:
                    winning_trades += 1
                else:
                    losing_trades += 1
                    
                peak_balance = max(peak_balance, balance)
                current_dd = ((peak_balance - balance) / peak_balance) * 100
                max_drawdown = max(max_drawdown, current_dd)
                
                in_trade = False
                continue

        # If not in trade, look for signals
        if not in_trade:
            X_live = row[extended_features].to_frame().T.astype(float)
            probabilities = strategy.model.predict_proba(X_live)[0]
            
            prob_down, prob_up = probabilities[0], probabilities[1]
            current_atr = row['ATRr_14']
            ema_200 = row['EMA_200']
            
            CONFIDENCE_THRESHOLD = 0.65
            
            if prob_up > CONFIDENCE_THRESHOLD and close_price > ema_200:
                trade_type = "BUY"
                in_trade = True
                entry_price = close_price
                sl = entry_price - (current_atr * atr_sl_mult)
                tp = entry_price + (current_atr * atr_tp_mult)
                sl_distance = abs(entry_price - sl)
                risk_amount = balance * (risk_percent / 100)
                lot_size = round(risk_amount / (sl_distance * 100000), 2)
                
            elif prob_down > CONFIDENCE_THRESHOLD and close_price < ema_200:
                trade_type = "SELL"
                in_trade = True
                entry_price = close_price
                sl = entry_price + (current_atr * atr_sl_mult)
                tp = entry_price - (current_atr * atr_tp_mult)
                sl_distance = abs(entry_price - sl)
                risk_amount = balance * (risk_percent / 100)
                lot_size = round(risk_amount / (sl_distance * 100000), 2)

    mt5.shutdown()
    
    # 3. Print Results
    logging.info("--- Backtest Complete ---")
    win_rate = (winning_trades / trades_taken) * 100 if trades_taken > 0 else 0
    net_profit = balance - initial_balance
    roi = (net_profit / initial_balance) * 100
    
    print("\n==============================")
    print(f"Total Trades: {trades_taken}")
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Winning Trades: {winning_trades}")
    print(f"Losing Trades: {losing_trades}")
    print(f"Initial Balance: ${initial_balance:.2f}")
    print(f"Final Balance: ${balance:.2f}")
    print(f"Net Profit: ${net_profit:.2f} ({roi:.2f}%)")
    print(f"Maximum Drawdown: {max_drawdown:.2f}%")
    print("==============================\n")

if __name__ == "__main__":
    run_backtest()
