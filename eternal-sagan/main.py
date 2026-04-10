import MetaTrader5 as mt5
import time
import logging
from strategy import MLHybridStrategy

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
SYMBOL = "EURUSD"
TIMEFRAME = mt5.TIMEFRAME_M15
RISK_PERCENT_PER_TRADE = 1.0  # Risk 1% of account balance
ATR_SL_MULT = 1.5             # Stop Loss distance = 1.5 * ATR
ATR_TP_MULT = 3.0             # Take Profit distance = 3.0 * ATR

def initialize_mt5():
    """Initialize connection to MetaTrader 5"""
    if not mt5.initialize():
        logging.error(f"Initialize failed, error code = {mt5.last_error()}")
        quit()
    logging.info("Connected to MetaTrader 5")
    
    # Ensure symbol is visible in Market Watch
    if not mt5.symbol_select(SYMBOL, True):
         logging.error(f"Failed to select symbol {SYMBOL}")
         quit()

def calculate_lot_size(sl_distance_points):
    """Calculate lot size based on account balance and risk percentage"""
    account_info = mt5.account_info()
    if account_info is None:
        logging.error("Failed to get account info.")
        return 0.01 # Fallback minimum lot size
        
    balance = account_info.margin_free
    risk_amount = balance * (RISK_PERCENT_PER_TRADE / 100)
    
    symbol_info = mt5.symbol_info(SYMBOL)
    tick_value = symbol_info.trade_tick_value
    tick_size = symbol_info.trade_tick_size
    
    if tick_value == 0.0 or tick_size == 0.0:
        return 0.01

    points_per_pip = 10 if symbol_info.digits in [3, 5] else 1
    
    # Points distance translated to risk cost per 1 standard lot
    tick_cost_per_lot = tick_value / tick_size
    total_risk_per_lot = sl_distance_points * tick_cost_per_lot
    
    if total_risk_per_lot <= 0: return 0.01
    
    lot_size = risk_amount / total_risk_per_lot
    
    # Bound lot size between min and max allowed by broker
    lot_size = max(symbol_info.volume_min, min(symbol_info.volume_max, lot_size))
    # Round to volume step
    step = symbol_info.volume_step
    lot_size = round(lot_size / step) * step
    
    return round(lot_size, 2)

def execute_trade(action, symbol, action_type, price, sl, tp):
    """Execute a trade on MT5 with advanced risk management"""
    symbol_info = mt5.symbol_info(symbol)
    point = symbol_info.point
    
    sl_distance_points = abs(price - sl) / point
    lot_size = calculate_lot_size(sl_distance_points)
    
    logging.info(f"Targeting Lot Size: {lot_size} based on {RISK_PERCENT_PER_TRADE}% risk. Risking amount distance: {sl_distance_points} points.")
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": action_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 10,  # 10 points max deviation or slippage
        "magic": 234001,
        "comment": "ML Bot Action",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logging.error(f"Order failed, retcode={result.retcode}")
        # Common error 10027: AutoTrading disabled by client
        if result.retcode == 10027:
            logging.error("AutoTrading is disabled in MT5 terminal. Please enable 'Algo trading'.")
        return None
        
    logging.info(f"Order successful! Ticket: {result.order}")
    return result

def run_bot():
    """Main autonomous loop"""
    initialize_mt5()
    
    # Instantiate the ML Strategy and train on the last 10,000 candles
    strategy = MLHybridStrategy(SYMBOL, TIMEFRAME, train_bars=10000)
    strategy.train()
    
    logging.info(f"Bot started. Autonomously trading {SYMBOL} using ML Model...")
    
    try:
        while True:
            # 1. Get market data & check for signals + Current Volatility (ATR)
            signal, current_atr = strategy.get_signal()
            
            # 2. Check current open positions
            positions = mt5.positions_get(symbol=SYMBOL, magic=234001)
            is_in_trade = False
            if positions is not None and len(positions) > 0:
                is_in_trade = True
            
            # 3. Execute logic based on signal
            if signal == "BUY" and not is_in_trade and current_atr > 0:
                ask = mt5.symbol_info_tick(SYMBOL).ask
                # SL/TP calculation based on ATR
                sl = ask - (current_atr * ATR_SL_MULT)
                tp = ask + (current_atr * ATR_TP_MULT)
                execute_trade("BUY", SYMBOL, mt5.ORDER_TYPE_BUY, ask, sl, tp)
                
            elif signal == "SELL" and not is_in_trade and current_atr > 0:
                bid = mt5.symbol_info_tick(SYMBOL).bid
                # SL/TP calculation based on ATR
                sl = bid + (current_atr * ATR_SL_MULT)
                tp = bid - (current_atr * ATR_TP_MULT)
                execute_trade("SELL", SYMBOL, mt5.ORDER_TYPE_SELL, bid, sl, tp)
            
            # Sleep until the next potential check (1 minute)
            time.sleep(60)
            
    except KeyboardInterrupt:
        logging.info("Bot stopped by user.")
    finally:
        mt5.shutdown()

if __name__ == "__main__":
    run_bot()
