import sys
sys.path.insert(0, '.')

# Test 1: imports
from core.mt5_gateway import MT5Gateway
from core.data_engine import DataEngine
from core.model_manager import ModelManager
from core.risk_engine import RiskEngine
from backtester.tick_sim import TickBacktester
print("PASS: All imports OK")

# Test 2: MT5 gateway
gw = MT5Gateway()
assert gw.connect(), "Gateway connect failed"
info = gw.get_account_info()
assert info is not None and "balance" in info
print(f"PASS: Gateway OK (Balance: ${info['balance']:,.2f})")

# Test 3: Data engine
import datetime
fetch_from = gw.get_server_time("EURUSD") - datetime.timedelta(seconds=120)
ticks = gw.get_ticks("EURUSD", fetch_from, 500)
engine = DataEngine()
features = engine.engineer_features(ticks)
assert features is not None, "DataEngine returned None"
print(f"PASS: DataEngine OK - features shape: {features.shape}")

# Test 4: Model prediction
brain = ModelManager()
feat_cols = ["velocity", "spread", "momentum_10", "momentum_50", "momentum_100"]
prob = brain.predict_probability(features[feat_cols])
assert 0 <= prob <= 1, f"Invalid probability: {prob}"
print(f"PASS: Model prediction OK - Confidence: {prob*100:.1f}%")

# Test 5: Risk engine
risk = RiskEngine()
sym = gw.get_symbol_info("EURUSD")
ok = risk.check_kill_switches(sym, ping_ms=2.0)
params = risk.get_order_params("EURUSD", "buy", sym["bid"], sym["ask"])
assert "price" in params and "sl" in params and "tp" in params
print(f"PASS: RiskEngine OK - Kill switch: {ok}")
print(f"      SL: {params['sl']:.5f} | TP: {params['tp']:.5f}")

gw.shutdown()
print("")
print("=== ALL SYSTEM CHECKS PASSED ===")
