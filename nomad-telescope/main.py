import time
import logging
from mt5_client import MT5Client
from strategy import HybridStrategy
from risk_manager import RiskManager
from position_manager import PositionManager
import config
import MetaTrader5 as mt5

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    client = MT5Client(login=config.MT5_LOGIN, password=config.MT5_PASSWORD, server=config.MT5_SERVER)
    if not client.connect():
        logging.error("Failed to connect to MT5. Ensure terminal is open. Exiting.")
        return

    # Track strategy state per symbol
    strategies = {sym: HybridStrategy(symbol=sym, htf=config.TIMEFRAME_HTF, ltf=config.TIMEFRAME_ENTRY) for sym in config.SYMBOLS}
    risk_manager = RiskManager(risk_percent=config.RISK_PER_TRADE_PERCENT, max_spread=config.MAX_SPREAD_POINTS)
    position_manager = PositionManager()

    logging.info(f"Starting HYBRID bot for {len(config.SYMBOLS)} symbols: {', '.join(config.SYMBOLS)}...")

    last_htf_update = 0
    last_heartbeat = time.time()
    HTF_UPDATE_INTERVAL = 60 * 15 # 15 minutes

    try:
        while True:
            current_time = time.time()
            
            # Update Higher Timeframe Regimes for all symbols
            if current_time - last_htf_update > HTF_UPDATE_INTERVAL:
                for symbol in config.SYMBOLS:
                    df_htf = client.get_candles(symbol, config.TIMEFRAME_HTF, 200)
                    regime, bias = strategies[symbol].analyze_htf(df_htf)
                    logging.info(f"[{symbol}] Regime Updated: {regime} | Bias: {bias}")
                last_htf_update = current_time

            for symbol in config.SYMBOLS:
                position_manager.move_to_breakeven(symbol, min_pips_profit=10)

                positions = mt5.positions_get(symbol=symbol)
                if positions is not None and len(positions) > 0:
                    continue # Already in a trade for this symbol

                df_ltf = client.get_candles(symbol, config.TIMEFRAME_ENTRY, 100)
                signal_data = strategies[symbol].find_ltf_entry(df_ltf)

                if signal_data:
                    tick = client.get_tick(symbol)
                    if not tick:
                        continue

                    symbol_info = mt5.symbol_info(symbol)
                    if symbol_info is None:
                        continue

                    spread_points = (tick.ask - tick.bid) / symbol_info.point
                    if spread_points > config.MAX_SPREAD_POINTS:
                        logging.warning(f"Spread too high on {symbol}: {spread_points}. Skipping.")
                        continue

                    account_info = mt5.account_info()
                    trade_mode = signal_data.get("type", "UNKNOWN")
                    
                    filling_type = mt5.ORDER_FILLING_FOK
                    if symbol_info.filling_mode & mt5.SYMBOL_FILLING_FOK:
                        filling_type = mt5.ORDER_FILLING_FOK
                    elif symbol_info.filling_mode & mt5.SYMBOL_FILLING_IOC:
                        filling_type = mt5.ORDER_FILLING_IOC
                    else:
                        filling_type = mt5.ORDER_FILLING_RETURN
                    
                    if signal_data['signal'] == "BUY":
                        entry_price = tick.ask
                        sl = signal_data['sl']
                        tp = signal_data['tp']
                        lot_size = risk_manager.calculate_lot_size(account_info.balance, entry_price, sl, symbol_info)
                        
                        request = {
                            "action": mt5.TRADE_ACTION_DEAL,
                            "symbol": symbol,
                            "volume": lot_size,
                            "type": mt5.ORDER_TYPE_BUY,
                            "price": entry_price,
                            "sl": sl,
                            "tp": tp,
                            "deviation": 10,
                            "magic": 123456,
                            "comment": f"BOT_B_{trade_mode}",
                            "type_time": mt5.ORDER_TIME_GTC,
                            "type_filling": filling_type,
                        }
                        result = mt5.order_send(request)
                        if result:
                            logging.info(f"BUY order sent for {symbol} [{trade_mode}]. Result: {result.comment}")

                    elif signal_data['signal'] == "SELL":
                        entry_price = tick.bid
                        sl = signal_data['sl']
                        tp = signal_data['tp']
                        lot_size = risk_manager.calculate_lot_size(account_info.balance, entry_price, sl, symbol_info)
                        
                        request = {
                            "action": mt5.TRADE_ACTION_DEAL,
                            "symbol": symbol,
                            "volume": lot_size,
                            "type": mt5.ORDER_TYPE_SELL,
                            "price": entry_price,
                            "sl": sl,
                            "tp": tp,
                            "deviation": 10,
                            "magic": 123456,
                            "comment": f"BOT_S_{trade_mode}",
                            "type_time": mt5.ORDER_TIME_GTC,
                            "type_filling": filling_type,
                        }
                        result = mt5.order_send(request)
                        if result:
                            logging.info(f"SELL order sent for {symbol} [{trade_mode}]. Result: {result.comment}")

            if current_time - last_heartbeat >= 60:
                logging.info("Heartbeat: Actively scanning LTF for valid setups...")
                last_heartbeat = current_time

            time.sleep(0.5) # Poll lightly

    except KeyboardInterrupt:
        logging.info("Shutting down bot...")
    finally:
        client.shutdown()

if __name__ == "__main__":
    main()
