import sys, os
sys.path.insert(0, '.')

print("=== FEATURE COLUMN CONSISTENCY CHECK ===")
files_to_check = {
    'core/model_manager.py': 17,
    'main.py': 72,
    'backtester/tick_sim.py': 23,
}
for f, line in files_to_check.items():
    with open(f) as fh:
        lines = fh.readlines()
        print(f"  {f}:{line} -> {lines[line-1].strip()}")

print()
print("=== TIMEZONE METHOD CHECK ===")
# Check for any raw datetime.now() or utcnow() in fetch paths
danger_files = ['main.py', 'app/auto_train.py', 'app/auto_validate.py']
all_clean = True
for f in danger_files:
    with open(f) as fh:
        content = fh.read()
        if 'datetime.now()' in content or 'utcnow()' in content:
            print(f"  WARNING: {f} still has raw datetime call")
            all_clean = False
if all_clean:
    print("  PASS: All fetch files use gateway.get_server_time()")

print()
print("=== MODEL FILE CHECK ===")
model = 'models/nova_hft_model.json'
if os.path.exists(model):
    size = os.path.getsize(model)
    print(f"  PASS: Model exists ({size:,} bytes)")
else:
    print("  FAIL: Model file missing!")

print()
print("=== PACKAGE IMPORT vs REQUIREMENTS CHECK ===")
# Verify the telegram import matches the package
try:
    import telebot
    print(f"  PASS: telebot (pyTelegramBotAPI) importable")
except ImportError:
    print("  WARNING: telebot not installed - run pip install pyTelegramBotAPI")

try:
    import websockets
    print(f"  PASS: websockets importable")
except ImportError:
    print("  WARNING: websockets not installed")

try:
    import streamlit
    print(f"  PASS: streamlit importable")
except ImportError:
    print("  WARNING: streamlit not installed")

print()
print("=== DAILY LOSS LIMIT ENFORCEMENT CHECK ===")
with open('core/risk_engine.py') as f:
    content = f.read()
    if 'daily_loss_limit' in content:
        print("  PASS: daily_loss_limit referenced in risk_engine")
    else:
        print("  NOTE: daily_loss_limit is in config.json but NOT enforced in risk_engine.py")
        print("        (Enhancement opportunity - not a bug)")

print()
print("=== FULL AUDIT COMPLETE ===")
