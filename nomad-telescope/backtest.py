import pandas as pd
import numpy as np
import logging
from mt5_client import MT5Client
import config
from ict_math import detect_fvg, detect_mss

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def calculate_adx(df: pd.DataFrame, period=42): # 42 M5 candles = 14 M15 candles approx
    df['tr1'] = df['high'] - df['low']
    df['tr2'] = abs(df['high'] - df['close'].shift(1))
    df['tr3'] = abs(df['low'] - df['close'].shift(1))
    df['tr'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
    
    df['plus_dm'] = np.where((df['high'] - df['high'].shift(1)) > (df['low'].shift(1) - df['low']), np.maximum(df['high'] - df['high'].shift(1), 0), 0)
    df['minus_dm'] = np.where((df['low'].shift(1) - df['low']) > (df['high'] - df['high'].shift(1)), np.maximum(df['low'].shift(1) - df['low'], 0), 0)
    
    atr = df['tr'].ewm(alpha=1/period, adjust=False).mean()
    df['plus_di'] = 100 * (df['plus_dm'].ewm(alpha=1/period, adjust=False).mean() / atr)
    df['minus_di'] = 100 * (df['minus_dm'].ewm(alpha=1/period, adjust=False).mean() / atr)
    
    dx = (abs(df['plus_di'] - df['minus_di']) / (df['plus_di'] + df['minus_di'])) * 100
    df['adx'] = dx.ewm(alpha=1/period, adjust=False).mean()
    return df

def run_hybrid_backtest(symbol="EURUSD", days=30):
    client = MT5Client(login=config.MT5_LOGIN, password=config.MT5_PASSWORD, server=config.MT5_SERVER)
    if not client.connect():
        logging.error("Failed to connect to MT5.")
        return

    logging.info(f"Downloading {days} days of M5 data for {symbol}...")
    num_m5 = days * 288
    df = client.get_candles(symbol, "M5", num_m5)
    client.shutdown()

    if df.empty: return

    logging.info("Processing Regime (ADX) and Bias...")
    df = calculate_adx(df, period=42) 
    df['sma_600'] = df['close'].rolling(window=600).mean() # Approx 200 SMA on M15
    df['Regime'] = np.where(df['adx'] > 25, 'TRENDING', 'RANGING')
    
    conditions = [df['close'] > df['sma_600'], df['close'] < df['sma_600']]
    choices = ['BULLISH', 'BEARISH']
    df['Bias'] = np.select(conditions, choices, default='NEUTRAL')
    
    logging.info("Processing Mean Reversion indicators...")
    period_mr = 20
    std_dev_multiplier = 2.2
    df['sma_20'] = df['close'].rolling(window=period_mr).mean()
    df['std_dev'] = df['close'].rolling(window=period_mr).std()
    df['upper_band'] = df['sma_20'] + (df['std_dev'] * std_dev_multiplier)
    df['lower_band'] = df['sma_20'] - (df['std_dev'] * std_dev_multiplier)
    
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi_14'] = 100 - (100 / (1 + rs))

    logging.info("Processing ICT Momentum indicators...")
    df = detect_mss(df, lookback=3)
    df = detect_fvg(df, min_fvg_pips=2.0, point_size=0.0001) 
    df['Recent_Bullish_FVG'] = df['Bullish_FVG'] | df['Bullish_FVG'].shift(1)
    df['Recent_Bearish_FVG'] = df['Bearish_FVG'] | df['Bearish_FVG'].shift(1)
    df['Rolling_Min_5'] = df['low'].rolling(5).min()
    df['Rolling_Max_5'] = df['high'].rolling(5).max()

    df['Buy_Signal'] = False
    df['Sell_Signal'] = False
    df['Entry_Price'] = 0.0
    df['SL'] = 0.0
    df['TP'] = 0.0
    df['Trade_Type'] = ""
    df['PNL_Win'] = 0.0
    df['PNL_Loss'] = 0.0

    logging.info("Generating signals...")
    for idx_name in df.index:
        idx = df.index.get_loc(idx_name)
        if idx < 600: continue
        
        row = df.iloc[idx]
        regime = row['Regime']
        bias = row['Bias']
        entry = row['close']
        
        # MEAN REVERSION REGIME
        if regime == "RANGING":
            if row['low'] <= row['lower_band'] and row['rsi_14'] < 30 and bias != "BEARISH":
                tp = row['sma_20']
                if tp > entry:
                    sl = entry - ((tp - entry) * 2.5)
                    df.at[idx_name, 'Buy_Signal'] = True
                    df.at[idx_name, 'Entry_Price'] = entry
                    df.at[idx_name, 'SL'] = sl
                    df.at[idx_name, 'TP'] = tp
                    df.at[idx_name, 'Trade_Type'] = "MR_BUY"
                    df.at[idx_name, 'PNL_Win'] = 1.0
                    df.at[idx_name, 'PNL_Loss'] = -2.5
            
            elif row['high'] >= row['upper_band'] and row['rsi_14'] > 70 and bias != "BULLISH":
                tp = row['sma_20']
                if tp < entry:
                    sl = entry + ((entry - tp) * 2.5)
                    df.at[idx_name, 'Sell_Signal'] = True
                    df.at[idx_name, 'Entry_Price'] = entry
                    df.at[idx_name, 'SL'] = sl
                    df.at[idx_name, 'TP'] = tp
                    df.at[idx_name, 'Trade_Type'] = "MR_SELL"
                    df.at[idx_name, 'PNL_Win'] = 1.0
                    df.at[idx_name, 'PNL_Loss'] = -2.5
                    
        # TRENDING REGIME (ICT Momentum)
        elif regime == "TRENDING":
            if bias == "BULLISH" and row['Recent_Bullish_FVG']:
                sl = row['Rolling_Min_5']
                if sl < entry:
                    tp = entry + ((entry - sl) * 3)
                    df.at[idx_name, 'Buy_Signal'] = True
                    df.at[idx_name, 'Entry_Price'] = entry
                    df.at[idx_name, 'SL'] = sl
                    df.at[idx_name, 'TP'] = tp
                    df.at[idx_name, 'Trade_Type'] = "ICT_BUY"
                    df.at[idx_name, 'PNL_Win'] = 3.0
                    df.at[idx_name, 'PNL_Loss'] = -1.0
            
            elif bias == "BEARISH" and row['Recent_Bearish_FVG']:
                sl = row['Rolling_Max_5']
                if sl > entry:
                    tp = entry - ((sl - entry) * 3)
                    df.at[idx_name, 'Sell_Signal'] = True
                    df.at[idx_name, 'Entry_Price'] = entry
                    df.at[idx_name, 'SL'] = sl
                    df.at[idx_name, 'TP'] = tp
                    df.at[idx_name, 'Trade_Type'] = "ICT_SELL"
                    df.at[idx_name, 'PNL_Win'] = 3.0
                    df.at[idx_name, 'PNL_Loss'] = -1.0

    logging.info("Simulating Hybrid trades forward...")
    trades = []
    in_trade = False
    trade_type = None
    trade_mode = ""
    sl = 0
    tp = 0
    entry_time = None
    pnl_win = 0
    pnl_loss = 0
    
    for i in range(len(df)):
        row = df.iloc[i]
        
        if in_trade:
            if trade_type == "BUY":
                if row['low'] <= sl:
                    trades.append({'mode': trade_mode, 'result': 'LOSS', 'pnl': pnl_loss})
                    in_trade = False
                elif row['high'] >= tp:
                    trades.append({'mode': trade_mode, 'result': 'WIN', 'pnl': pnl_win})
                    in_trade = False
            elif trade_type == "SELL":
                if row['high'] >= sl:
                    trades.append({'mode': trade_mode, 'result': 'LOSS', 'pnl': pnl_loss})
                    in_trade = False
                elif row['low'] <= tp:
                    trades.append({'mode': trade_mode, 'result': 'WIN', 'pnl': pnl_win})
                    in_trade = False
        
        if not in_trade:
            if row['Buy_Signal']:
                in_trade = True
                trade_type = "BUY"
                trade_mode = row['Trade_Type']
                sl = row['SL']
                tp = row['TP']
                pnl_win = row['PNL_Win']
                pnl_loss = row['PNL_Loss']
            elif row['Sell_Signal']:
                in_trade = True
                trade_type = "SELL"
                trade_mode = row['Trade_Type']
                sl = row['SL']
                tp = row['TP']
                pnl_win = row['PNL_Win']
                pnl_loss = row['PNL_Loss']
                
    if not trades:
        logging.info("No trades taken.")
        return
        
    df_trades = pd.DataFrame(trades)
    mr_trades = df_trades[df_trades['mode'].str.startswith('MR')]
    ict_trades = df_trades[df_trades['mode'].str.startswith('ICT')]
    
    print("\n" + "="*50)
    print("BACKTEST RESULTS (Hybrid Regime Bot - M5/M15)")
    print("="*50)
    print(f"Symbol:           {symbol}")
    print(f"Period:           {days} Days")
    print(f"Total Trades:     {len(df_trades)}")
    print(f"Total Net Return: {df_trades['pnl'].sum():.2f} R")
    print("-" * 50)
    
    if len(mr_trades) > 0:
        mr_wins = len(mr_trades[mr_trades['result'] == 'WIN'])
        mr_winrate = (mr_wins / len(mr_trades)) * 100
        print(f"[Ranging] Mean Reversion Trades: {len(mr_trades)}")
        print(f"          Win Rate: {mr_winrate:.2f}% | PnL: {mr_trades['pnl'].sum():.2f} R")
    else:
        print("[Ranging] Mean Reversion Trades: 0")
        
    if len(ict_trades) > 0:
        ict_wins = len(ict_trades[ict_trades['result'] == 'WIN'])
        ict_winrate = (ict_wins / len(ict_trades)) * 100
        print(f"[Trending] ICT Momentum Trades:  {len(ict_trades)}")
        print(f"           Win Rate: {ict_winrate:.2f}% | PnL: {ict_trades['pnl'].sum():.2f} R")
    else:
        print("[Trending] ICT Momentum Trades: 0")
    print("="*50)

if __name__ == "__main__":
    for sym in config.SYMBOLS:
        run_hybrid_backtest(sym, days=30)
