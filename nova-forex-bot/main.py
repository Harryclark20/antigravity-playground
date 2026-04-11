from core.mt5_gateway import MT5Gateway
from core.data_engine import DataEngine
from core.model_manager import ModelManager
from core.risk_engine import RiskEngine
import datetime

def main():
    print("--- Nova HFT Bot (Powered by Tick-Level AI) ---")
    
    gateway = MT5Gateway()
    engine = DataEngine()
    brain = ModelManager()
    risk = RiskEngine()
    
    symbol = "EURUSD" # Focused HFT universe
    
    if gateway.connect():
        try:
            print(f"Monitoring {symbol} for tick velocity bursts...")
            
            while True:
                # 1. Fetch Tick Window (Last 1000 ticks)
                ticks = gateway.get_ticks(symbol, datetime.datetime.now(), 1000)
                
                # 2. Extract Micro-Features
                features = engine.engineer_features(ticks)
                
                if features is not None:
                    # 3. Get AI Alpha Prediction
                    prob = brain.predict_probability(features[['velocity', 'spread', 'momentum_10', 'momentum_50', 'momentum_100', 'vol_imbalance']])
                    
                    if prob > 0.8: # high confidence threshold
                        print(f"ALPHA DETECTED: Probability {prob:.2f}. Checking Shield...")
                        
                        # 4. Check Risk Kill-Switches
                        symbol_info = gateway.get_symbol_info(symbol)
                        if risk.check_kill_switches(symbol_info, ping_ms=2.0): # Mocking ping
                            print("EXECUTION GRANTED. Routing Order...")
                            # (mt5.order_send logic would be triggered here)
                
                time.sleep(0.5) # Sub-second frequency control
                
        except KeyboardInterrupt:
            print("Emergency stop triggered.")
        finally:
            gateway.shutdown()
    else:
        print("Could not initialize live infrastructure.")

if __name__ == "__main__":
    main()
 Riverside, CA
