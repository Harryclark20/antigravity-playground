import MetaTrader5 as mt5
from core.mt5_gateway import MT5Gateway
from core.data_engine import DataEngine
from core.model_manager import ModelManager
from core.risk_engine import RiskEngine
from core.broadcaster import Broadcaster
from core.telegram_agent import TelegramAgent
import datetime
import time

def main():
    print("--- Nova HFT Bot: PRODUCTION LIVE ENGINE ---")
    
    # ===================================================
    # CONFIGURATION
    # Set LIVE_TRADING_ENABLED = True ONLY after running
    # auto_validate.py and reviewing the performance report.
    # ===================================================
    LIVE_TRADING_ENABLED = True
    
    # Load multi-symbol configuration
    import json
    with open('config.json', 'r') as f:
        bot_config = json.load(f)
    SYMBOLS = bot_config['trading']['symbols']
    
    CONFIDENCE_THRESHOLD = 0.65
    TICK_LOOKBACK = 500       # Ticks fed to the DataEngine per cycle
    LOOP_SLEEP_SEC = 0.1      # 100ms precision loop

    # Instantiate all modules
    gateway = MT5Gateway()
    engine = DataEngine()
    brain = ModelManager()
    risk = RiskEngine()
    broadcaster = Broadcaster()
    telegram = TelegramAgent()

    # Remote command callback (called from Telegram polling thread)
    def handle_remote_command(command):
        nonlocal LIVE_TRADING_ENABLED
        if command == "pause":
            LIVE_TRADING_ENABLED = False
            print("[Remote] Trading PAUSED via Telegram.")
        elif command == "status":
            info = gateway.get_account_info()
            if info:
                telegram.send_alert(
                    f"📊 STATUS\n"
                    f"Balance: ${info['balance']:.2f}\n"
                    f"Equity:  ${info['equity']:.2f}\n"
                    f"Live Trading: {'ON' if LIVE_TRADING_ENABLED else 'OFF'}"
                )

    telegram.register_callback(handle_remote_command)

    MAGIC = bot_config['trading']['magic_number']
    
    if not gateway.connect():
        print("FATAL: Infrastructure failed to initialize. Exiting.")
        return

    try:
        print(f"HFT Engine Active. Monitoring {', '.join(SYMBOLS)}...")
        telegram.send_alert("🚀 Nova HFT System Online and Monitoring.")
        
        last_log_time = 0
        last_ui_time = 0
        last_safety_time = 0
        consecutive_losses = 0
        cooling_until = 0

        while True:
            current_time = time.time()
            is_cooling = current_time < cooling_until
            
            # --- 0. Periodic Safety & Circuit Breaker (Every 30s) ---
            if not is_cooling and (current_time - last_safety_time > 30):
                last_safety_time = current_time
                history = mt5.history_deals_get(datetime.datetime.now() - datetime.timedelta(hours=1), datetime.datetime.now())
                if history:
                    # Filter for deals related to our MAGIC number
                    deals = sorted([d for d in history if d.magic == MAGIC], key=lambda x: x.time, reverse=True)
                    last_3 = [d for d in deals if d.entry == mt5.DEAL_ENTRY_OUT][:3]
                    if len(last_3) >= 3 and all(d.profit < 0 for d in last_3):
                        cooling_until = current_time + (30 * 60) # 30 min cooling
                        print(f"!!! CIRCUIT BREAKER TRIPPED !!! 3 consecutive losses detected. Cooling down for 30m.")
                        telegram.send_alert("⚠️ CIRCUIT BREAKER: 3 consecutive losses. Cooling down for 30 minutes.")
                        is_cooling = True

            for symbol in SYMBOLS:
                # --- 1. Position Tracking (Filtered by MAGIC) ---
                positions = mt5.positions_get(symbol=symbol)
                # Filter positions by our magic number to avoid manual trade interference
                bot_positions = [p for p in positions if p.magic == MAGIC] if positions else []
                current_pnl = sum(p.profit for p in bot_positions) if bot_positions else 0.0

                # --- 2. Fetch & Process Ticks ---
                ticks = gateway.get_ticks(symbol, TICK_LOOKBACK, time_window_minutes=60)
                features = engine.engineer_features(ticks)
                
                if features is not None:
                    # --- 3. AI Prediction ---
                    feat_cols = ['velocity', 'spread', 'momentum_10', 'momentum_50', 'momentum_100', 'rsi_50', 'bb_zscore']
                    prob = brain.predict_probability(features[feat_cols])
                    vol = float(features.iloc[0]['volatility'])

                    # --- 4. Throttled UI Broadcast (Every 5s) ---
                    if current_time - last_ui_time > 5:
                        symbol_info = gateway.get_symbol_info(symbol)
                        acct_info = gateway.get_account_info()
                        start_balance = acct_info['balance'] if acct_info else 10000.0
                        drawdown_pct = ((start_balance - acct_info['equity']) / start_balance * 100) if acct_info else 0.0

                        history_data = []
                        for i in range(min(50, len(ticks))):
                            history_data.append({
                                "time": datetime.datetime.fromtimestamp(ticks[-i-1]['time_msc']/1000).strftime('%H:%M:%S'),
                                "price": (ticks[-i-1]['bid'] + ticks[-i-1]['ask'])/2
                            })
                        history_data.reverse()

                        broadcaster.broadcast({
                            "symbol": symbol,
                            "account": acct_info,
                            "health": {"ping": gateway.get_latency(active=True), "velocity": float(features.iloc[0]['velocity']), "volatility": vol},
                            "equity": {"balance": start_balance, "drawdown": round(drawdown_pct, 3), "pnl": round(current_pnl, 2)},
                            "ai": {"confidence": round(float(prob), 4), "spread": symbol_info['spread'] if symbol_info else 0},
                            "chart": history_data
                        })
                        if symbol == SYMBOLS[-1]: last_ui_time = current_time

                    # --- 5. Execution Logic (Bidirectional) ---
                    if not bot_positions and not is_cooling:
                        direction = None
                        if prob > CONFIDENCE_THRESHOLD:
                            direction = 'buy'
                        elif prob < (1 - CONFIDENCE_THRESHOLD):
                            direction = 'sell'
                        
                        if direction:
                            symbol_info = gateway.get_symbol_info(symbol)
                            latency = gateway.get_latency(active=True)
                            
                            if symbol_info and risk.check_kill_switches(symbol_info, ping_ms=latency):
                                params = risk.get_order_params(
                                    symbol, direction, symbol_info['bid'], symbol_info['ask'], volatility=vol
                                )

                                if LIVE_TRADING_ENABLED:
                                    order_type = mt5.ORDER_TYPE_BUY if direction == 'buy' else mt5.ORDER_TYPE_SELL
                                    # For short, Kelly should use the probability of the drop (1-prob)
                                    k_prob = prob if direction == 'buy' else (1.0 - prob)
                                    
                                    request = {
                                        "action": mt5.TRADE_ACTION_DEAL,
                                        "symbol": symbol,
                                        "volume": risk.calculate_lot_size(start_balance, prob=k_prob),
                                        "type": order_type,
                                        "price": params['price'],
                                        "sl": params['sl'],
                                        "tp": params['tp'],
                                        "magic": MAGIC,
                                        "comment": f"Nova HFT {direction.upper()} Vol-Dyn",
                                        "type_time": mt5.ORDER_TIME_GTC,
                                        "type_filling": mt5.ORDER_FILLING_IOC,
                                    }
                                    result = mt5.order_send(request)
                                    if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                                        telegram.send_alert(
                                            f"🚀 {direction.upper()} OPENED [{symbol}]\n"
                                            f"Price: {params['price']}\n"
                                            f"SL: {params['sl']:.5f} | TP: {params['tp']:.5f}\n"
                                            f"AI Conf: {k_prob*100:.1f}%"
                                        )
                                    else:
                                        err_msg = mt5.last_error() if not result else f"Retcode: {result.retcode}"
                                        print(f"Execution Failed: {err_msg}")
                                else:
                                    print(f"[VIRTUAL] {symbol} {direction.upper()} signal at {prob:.4f}")

                # --- 6. Throttled Heartbeat Log ---
                if current_time - last_log_time > 15:
                    if features is None:
                        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {symbol}: Awaiting volume...")
                    else:
                        cool_str = " | [COOLING]" if is_cooling else ""
                        status = "Monitoring..." if not (prob > CONFIDENCE_THRESHOLD or prob < (1-CONFIDENCE_THRESHOLD)) else "SIGNAL!"
                        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {symbol} ({status}) | Conf: {prob*100:.1f}% | Vol: {vol:.6f}{cool_str}")
                    
                    if symbol == SYMBOLS[-1]: last_log_time = current_time
            
            time.sleep(LOOP_SLEEP_SEC)

    except KeyboardInterrupt:
        print("\nSystem Halted by user.")
        telegram.send_alert("🔴 Nova HFT HALTED MANUALLY.")
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        telegram.send_alert(f"🚨 CRITICAL ERROR: {e}")
    finally:
        gateway.shutdown()
        print("MT5 connection closed.")

if __name__ == "__main__":
    main()
