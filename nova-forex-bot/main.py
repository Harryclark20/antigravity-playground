import MetaTrader5 as mt5
from core.mt5_gateway import MT5Gateway
from core.data_engine import DataEngine
from core.model_manager import ModelManager
from core.risk_engine import RiskEngine
import datetime
import time

def main():
    print("--- Nova HFT Bot: PRODUCTION LIVE ENGINE ---")
    
    # --- CONFIGURATION ---
    LIVE_TRADING_ENABLED = False # Safety set to False by default
    SYMBOL = "EURUSD"
    CONFIDENCE_THRESHOLD = 0.85
    # ---------------------

    gateway = MT5Gateway()
    engine = DataEngine()
    brain = ModelManager()
    risk = RiskEngine()
    
    if gateway.connect():
        try:
            print(f"HFT Engine Active. Monitoring {SYMBOL}...")
            
            while True:
                # 1. Position Tracking (Only 1 trade at a time)
                positions = mt5.positions_get(symbol=SYMBOL)
                if len(positions) > 0:
                    time.sleep(1)
                    continue

                # 2. Fetch & Process Ticks
                ticks = gateway.get_ticks(SYMBOL, datetime.datetime.now(), 500)
                features = engine.engineer_features(ticks)
                
                if features is not None:
                    # 3. AI Prediction
                    prob = brain.predict_probability(features[['velocity', 'spread', 'momentum_10', 'momentum_50', 'momentum_100', 'vol_imbalance']])
                    
                    if prob > CONFIDENCE_THRESHOLD:
                        print(f"[{datetime.datetime.now()}] SIGNAL: {prob*100:.1f}% Confidence.")
                        
                        symbol_info = gateway.get_symbol_info(SYMBOL)
                        if risk.check_kill_switches(symbol_info, ping_ms=1.5):
                            
                            params = risk.get_order_params(SYMBOL, 'buy', symbol_info['bid'], symbol_info['ask'])
                            
                            if LIVE_TRADING_ENABLED:
                                print(f"AUTOPILOT: Executing BUY at {params['price']}...")
                                request = {
                                    "action": mt5.TRADE_ACTION_DEAL,
                                    "symbol": SYMBOL,
                                    "volume": risk.calculate_lot_size(10000), # Mock balance
                                    "type": mt5.ORDER_TYPE_BUY,
                                    "price": params['price'],
                                    "sl": params['sl'],
                                    "tp": params['tp'],
                                    "magic": 123456,
                                    "comment": "Nova HFT Autopilot",
                                    "type_time": mt5.ORDER_TIME_GTC,
                                    "type_filling": mt5.ORDER_FILLING_IOC,
                                }
                                result = mt5.order_send(request)
                                if result.retcode != mt5.TRADE_RETCODE_DONE:
                                    print(f"Execution Error: {result.retcode}")
                            else:
                                print("VIRTUAL SIGNAL: Trade would have triggered here (Live mode is OFF).")
                
                time.sleep(0.1) # Precision frequency
                
        except KeyboardInterrupt:
            print("System Halted.")
        finally:
            gateway.shutdown()
    else:
        print("Infrastructure failed to initialize.")

if __name__ == "__main__":
    main()
