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
    LIVE_TRADING_ENABLED = False
    SYMBOL = "EURUSD"
    CONFIDENCE_THRESHOLD = 0.85
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

    if not gateway.connect():
        print("FATAL: Infrastructure failed to initialize. Exiting.")
        return

    try:
        print(f"HFT Engine Active. Monitoring {SYMBOL}...")
        telegram.send_alert("🚀 Nova HFT System Online and Monitoring.")

        while True:
            # --- 1. Position Tracking ---
            positions = mt5.positions_get(symbol=SYMBOL)
            current_pnl = sum(p.profit for p in positions) if positions else 0.0

            # --- 2. Fetch & Process Ticks ---
            # Fetch recent ticks anchored to broker server time (timezone-safe)
            fetch_from = gateway.get_server_time(SYMBOL) - datetime.timedelta(seconds=60)
            ticks = gateway.get_ticks(SYMBOL, fetch_from, TICK_LOOKBACK)
            features = engine.engineer_features(ticks)

            if features is not None:
                # --- 3. AI Prediction ---
                feat_cols = ['velocity', 'spread', 'momentum_10', 'momentum_50', 'momentum_100']
                prob = brain.predict_probability(features[feat_cols])

                # --- 4. Broadcast to Dashboard ---
                symbol_info = gateway.get_symbol_info(SYMBOL)
                acct_info = gateway.get_account_info()
                start_balance = acct_info['balance'] if acct_info else 10000.0
                drawdown_pct = ((start_balance - acct_info['equity']) / start_balance * 100) if acct_info else 0.0

                # Calculate history pulse for the chart
                history_data = []
                for i in range(min(50, len(ticks))):
                    history_data.append({
                        "time": datetime.datetime.fromtimestamp(ticks[-i-1]['time_msc']/1000).strftime('%H:%M:%S'),
                        "price": (ticks[-i-1]['bid'] + ticks[-i-1]['ask'])/2
                    })
                history_data.reverse()

                broadcaster.broadcast({
                    "account": acct_info,
                    "health": {
                        "ping": 2,  
                        "velocity": float(features.iloc[0]['velocity'])
                    },
                    "equity": {
                        "balance": start_balance,
                        "drawdown": round(drawdown_pct, 3),
                        "pnl": round(current_pnl, 2)
                    },
                    "ai": {
                        "confidence": round(float(prob), 4),
                        "spread": symbol_info['spread'] if symbol_info else 0
                    },
                    "chart": history_data
                })

                # --- 5. Execution Logic (only 1 position max) ---
                if prob > CONFIDENCE_THRESHOLD and not positions:
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] SIGNAL: {prob*100:.1f}% Confidence.")

                    if symbol_info and risk.check_kill_switches(symbol_info, ping_ms=2.0):
                        params = risk.get_order_params(
                            SYMBOL, 'buy', symbol_info['bid'], symbol_info['ask']
                        )

                        if LIVE_TRADING_ENABLED:
                            request = {
                                "action": mt5.TRADE_ACTION_DEAL,
                                "symbol": SYMBOL,
                                "volume": risk.calculate_lot_size(start_balance),
                                "type": mt5.ORDER_TYPE_BUY,
                                "price": params['price'],
                                "sl": params['sl'],
                                "tp": params['tp'],
                                "magic": 123456,
                                "comment": "Nova HFT",
                                "type_time": mt5.ORDER_TIME_GTC,
                                "type_filling": mt5.ORDER_FILLING_IOC,
                            }
                            result = mt5.order_send(request)
                            if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                                telegram.send_alert(
                                    f"📈 LONG OPENED\n"
                                    f"Symbol: {SYMBOL}\n"
                                    f"Price:  {params['price']}\n"
                                    f"SL: {params['sl']} | TP: {params['tp']}\n"
                                    f"AI Conf: {prob*100:.1f}%"
                                )
                            else:
                                code = result.retcode if result else "N/A"
                                print(f"Order failed. Retcode: {code}")
                        else:
                            print("  [VIRTUAL] Live mode is OFF — signal logged only.")

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
