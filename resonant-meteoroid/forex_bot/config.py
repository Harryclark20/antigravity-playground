import os

# --- MT5 Connection ---
MT5_ACCOUNT = 5047825822  # Replace with actual account number
MT5_PASSWORD = "RpUaG_K5"
MT5_SERVER = "MetaQuotes-Demo"
MT5_PATH = "C:/Program Files/MetaTrader 5/terminal64.exe"  # Optional: path to terminal.exe if multiple installed

# --- Traded Symbols ---
SYMBOLS = ["XAUUSD", "GBPJPY"]
TIMEFRAME = 15  # Minutes

# --- Risk Management ---
RISK_PER_TRADE_PERCENT = 1.0  # Default 1%
MAX_DAILY_LOSS_PERCENT = 3.0
MAX_TRADES_PER_DAY = 10
MAX_CONSECUTIVE_LOSSES = 3

# --- Signals & AI ---
MIN_VOTES_REQUIRED = 2  # Allows specialized strategies (Weight 2) to trigger high-quality solo setups
AI_PROBABILITY_THRESHOLD = 0.70  # Increased threshold to 70% for the $50 account protection
MIN_SIGNAL_CONFIDENCE = 0.70  # Require strong combined confidence before trading
MIN_RISK_REWARD_RATIO = 2.0  # Enforce at least 2:1 reward:risk

# --- Indicators Settings ---
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

# --- File Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
ANALYTICS_DIR = os.path.join(BASE_DIR, "analytics")

for dir_path in [LOGS_DIR, DATA_DIR, MODELS_DIR, ANALYTICS_DIR]:
    os.makedirs(dir_path, exist_ok=True)
