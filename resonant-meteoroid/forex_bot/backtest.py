import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np
import os
import logging
from datetime import datetime

# Import the existing bot logic
from config import ANALYTICS_DIR, MIN_VOTES_REQUIRED, SYMBOLS
from strategies.regime_detector import RegimeDetector
from strategies.trend_pullback import TrendPullbackStrategy
from strategies.mean_reversion import MeanReversionStrategy
from strategies.liquidity_sweep import LiquiditySweepStrategy
from strategies.breakout_expansion import BreakoutExpansionStrategy
from strategies.session_momentum import SessionMomentumStrategy
from strategies.volatility_sniper import VolatilitySniperStrategy
from strategies.xau_volatility_breakout import PreciousMetalsVolatilityBreakoutStrategy
from strategies.voter import SignalVoter

# Hardcode some configuration equivalents for offline calculations
EMA_FAST = 20
EMA_MEDIUM = 50
EMA_SLOW = 200
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
ATR_PERIOD = 14
ADX_PERIOD = 14
BOLLINGER_PERIOD = 20
BOLLINGER_STD_DEV = 2.0
DONCHIAN_PERIOD = 20

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def download_data(symbol, interval='15m', period='60d'):
    """Fetch offline data using yfinance for backtesting."""
    # Convert MT5 symbol to yfinance format
    if symbol == "XAUUSD":
        yf_symbol = "GC=F" # Gold Futures
    elif symbol == "XAGUSD":
        yf_symbol = "SI=F" # Silver Futures
    elif symbol == "BTCUSD":
        yf_symbol = "BTC-USD"
    else:
        yf_symbol = f"{symbol}=X"
        
    logger.info(f"Downloading {period} of {interval} data for {yf_symbol}...")
    df = yf.download(yf_symbol, interval=interval, period=period, progress=False)
    
    if df.empty:
        logger.error(f"Failed to fetch data for {yf_symbol}")
        return None

    # Handle yfinance multi-index columns if they exist
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Rename columns to match MT5 expected format
    df.rename(columns={
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'tick_volume'
    }, inplace=True)
    
    return df

def compute_indicators(df):
    """Calculate the exact same indicators used by the DataEngine"""
    logger.info("Computing indicators...")
    # EMAs
    df['EMA_20'] = ta.ema(df['close'], length=EMA_FAST)
    df['EMA_50'] = ta.ema(df['close'], length=EMA_MEDIUM)
    df['EMA_200'] = ta.ema(df['close'], length=EMA_SLOW)

    # RSI
    df['RSI'] = ta.rsi(df['close'], length=RSI_PERIOD)

    # MACD
    macd = ta.macd(df['close'], fast=MACD_FAST, slow=MACD_SLOW, signal=MACD_SIGNAL)
    if macd is not None and not macd.empty:
        df = df.join(macd)
        df.rename(columns={
            f'MACD_{MACD_FAST}_{MACD_SLOW}_{MACD_SIGNAL}': 'MACD',
            f'MACDh_{MACD_FAST}_{MACD_SLOW}_{MACD_SIGNAL}': 'MACD_hist',
            f'MACDs_{MACD_FAST}_{MACD_SLOW}_{MACD_SIGNAL}': 'MACD_signal'
        }, inplace=True)

    # ATR
    df['ATR'] = ta.atr(df['high'], df['low'], df['close'], length=ATR_PERIOD)

    # ADX
    adx = ta.adx(df['high'], df['low'], df['close'], length=ADX_PERIOD)
    if adx is not None and not adx.empty:
        df = df.join(adx)
        df.rename(columns={
            f'ADX_{ADX_PERIOD}': 'ADX',
            f'DMP_{ADX_PERIOD}': 'DI_plus',
            f'DMN_{ADX_PERIOD}': 'DI_minus'
        }, inplace=True)

    # Bollinger Bands
    bb = ta.bbands(df['close'], length=BOLLINGER_PERIOD, std=BOLLINGER_STD_DEV)
    if bb is not None and not bb.empty:
        df = df.join(bb)
        df.rename(columns={
            f'BBL_{BOLLINGER_PERIOD}_{BOLLINGER_STD_DEV}_{BOLLINGER_STD_DEV}': 'BB_lower',
            f'BBM_{BOLLINGER_PERIOD}_{BOLLINGER_STD_DEV}_{BOLLINGER_STD_DEV}': 'BB_middle',
            f'BBU_{BOLLINGER_PERIOD}_{BOLLINGER_STD_DEV}_{BOLLINGER_STD_DEV}': 'BB_upper',
            f'BBB_{BOLLINGER_PERIOD}_{BOLLINGER_STD_DEV}_{BOLLINGER_STD_DEV}': 'BB_bandwidth',
            f'BBP_{BOLLINGER_PERIOD}_{BOLLINGER_STD_DEV}_{BOLLINGER_STD_DEV}': 'BB_percent'
        }, inplace=True)

    # Donchian Channel
    dc = ta.donchian(df['high'], df['low'], lower_length=DONCHIAN_PERIOD, upper_length=DONCHIAN_PERIOD)
    if dc is not None and not dc.empty:
        df = df.join(dc)
        df.rename(columns={
            f'DCL_{DONCHIAN_PERIOD}_{DONCHIAN_PERIOD}': 'DC_lower',
            f'DCM_{DONCHIAN_PERIOD}_{DONCHIAN_PERIOD}': 'DC_middle',
            f'DCU_{DONCHIAN_PERIOD}_{DONCHIAN_PERIOD}': 'DC_upper'
        }, inplace=True)

    # VWAP Proxy
    try:
        vwap = ta.vwap(df['high'], df['low'], df['close'], df['tick_volume'])
        df['VWAP'] = vwap
    except:
        df['VWAP'] = df['close'] # fallback
        
    df['VWAP'] = df['VWAP'].fillna(df['close'])
    return df.dropna()


def run_backtest(symbol):
    df = download_data(symbol)
    if df is None: return
    df = compute_indicators(df)

    regime_detector = RegimeDetector()
    strategies = {
        'trend': TrendPullbackStrategy(),
        'mean_rev': MeanReversionStrategy(),
        'liquidity': LiquiditySweepStrategy(),
        'breakout': BreakoutExpansionStrategy(),
        'momentum': SessionMomentumStrategy(),
        'sniper': VolatilitySniperStrategy(),
        'xau_breakout': PreciousMetalsVolatilityBreakoutStrategy()
    }
    voter = SignalVoter(min_votes=2) # Requiring at least 2 strategies to agree for higher probability signals

    # Simulated Account Iteration
    balance = 10000.0
    risk_per_trade = 0.01
    
    open_trades = []
    trade_history = []
    
    logger.info(f"Starting Offline Simulation for {symbol} on {len(df)} candles...")
    
    for i in range(200, len(df)):
        # Provide the dataframe up to the current candle
        window = df.iloc[:i+1]
        current_candle = window.iloc[-1]
        current_time = window.index[-1]
        current_price = current_candle['close']
        
        # 1. Manage existing trades (Check Stops/TP)
        for trade in open_trades[:]:
            closed = False
            profit = 0
            
            if trade['type'] == 'BUY':
                if current_candle['low'] <= trade['sl']:
                    profit = -balance * risk_per_trade
                    closed = True
                    trade['exit_reason'] = 'SL'
                elif current_candle['high'] >= trade['tp']:
                    reward_ratio = (trade['tp'] - trade['entry_price']) / (trade['entry_price'] - trade['sl'])
                    profit = (balance * risk_per_trade) * reward_ratio
                    closed = True
                    trade['exit_reason'] = 'TP'
                    
            elif trade['type'] == 'SELL':
                if current_candle['high'] >= trade['sl']:
                    profit = -balance * risk_per_trade
                    closed = True
                    trade['exit_reason'] = 'SL'
                elif current_candle['low'] <= trade['tp']:
                    reward_ratio = (trade['entry_price'] - trade['tp']) / (trade['sl'] - trade['entry_price'])
                    profit = (balance * risk_per_trade) * reward_ratio
                    closed = True
                    trade['exit_reason'] = 'TP'
                    
            if closed:
                balance += profit
                trade['exit_time'] = current_time
                trade['profit'] = profit
                trade['success'] = 1 if profit > 0 else 0
                trade['balance_after'] = balance
                trade_history.append(trade)
                open_trades.remove(trade)
                
        # 2. Check for new signals
        # Don't open identical concurrent trades to avoid margin stacking in backtest
        if len(open_trades) > 0:
            continue

        regime = regime_detector.detect(window)
        if regime == "TREND":
            active_strategies = ['trend', 'breakout', 'momentum', 'xau_breakout']
        elif regime == "RANGE":
            active_strategies = ['mean_rev', 'liquidity']
        elif regime == "VOLATILE":
            active_strategies = ['sniper', 'breakout', 'mean_rev', 'xau_breakout']
        elif regime == "LOW VOLATILITY":
            active_strategies = ['sniper', 'breakout']
        else:
            active_strategies = list(strategies.keys())

        results = {}
        for name in active_strategies:
            strat_result = strategies[name].analyze(window)
            # Ensure parity with main.py weighting logic
            results[name] = strat_result
            
        vote = voter.evaluate(results)
        
        if vote['signal'] != 'NO_TRADE':
            # Execute Simulated Trade
            signal = vote['signal']
            sl_dist = vote['sl_distance']
            tp_dist = vote['tp_distance']
            
            # Require valid SL/TP
            if sl_dist <= 0 or tp_dist <= 0:
                continue
                
            sl_price = current_price - sl_dist if signal == 'BUY' else current_price + sl_dist
            tp_price = current_price + tp_dist if signal == 'BUY' else current_price - tp_dist
            
            new_trade = {
                'entry_time': current_time,
                'symbol': symbol,
                'type': signal,
                'entry_price': current_price,
                'sl': sl_price,
                'tp': tp_price,
                'regime': regime,
                # Feature states for AI Training
                'RSI': current_candle.get('RSI', 50),
                'ATR': current_candle.get('ATR', 0),
                'ADX': current_candle.get('ADX', 15),
                'dist_ema50': (current_price - current_candle.get('EMA_50', current_price)) / current_price,
                'volatility_bb': current_candle.get('BB_bandwidth', 0),
                'session_hour': current_time.hour
            }
            open_trades.append(new_trade)

    # Process metrics
    if len(trade_history) > 0:
        history_df = pd.DataFrame(trade_history)
        wins = history_df[history_df['success'] == 1]
        losses = history_df[history_df['success'] == 0]
        
        win_rate = len(wins) / len(history_df) * 100
        total_p = wins['profit'].sum()
        total_l = abs(losses['profit'].sum())
        profit_factor = total_p / total_l if total_l > 0 else float('inf')
        
        logger.info(f"\n--- Backtest Results: {symbol} ---")
        logger.info(f"Total Trades: {len(history_df)}")
        logger.info(f"Win Rate: {win_rate:.1f}%")
        logger.info(f"Ending Balance: ${balance:.2f} (Start: $10000)")
        logger.info(f"Profit Factor: {profit_factor:.2f}")
        
        # Save to csv to fulfill the AI training requirement
        out_path = os.path.join(ANALYTICS_DIR, "trades_history.csv")
        os.makedirs(ANALYTICS_DIR, exist_ok=True)
        history_df.to_csv(out_path, index=False)
        logger.info(f"Saved trade data to {out_path} for AI Bootstrapping.")
    else:
        logger.info(f"No trades executed for {symbol} under current logic constraints.")

if __name__ == "__main__":
    # Testing on major momentum and volatile pairs
    for sym in ["EURUSD", "GBPJPY", "XAUUSD", "XAGUSD", "BTCUSD"]:
        run_backtest(sym)
