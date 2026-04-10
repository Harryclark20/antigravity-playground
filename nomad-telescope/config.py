import os

# MT5 Connection Settings
# By default we assume the terminal is already logged into the correct account,
# but we can provide explicit credentials here.
MT5_LOGIN = os.getenv("MT5_LOGIN", "")
MT5_PASSWORD = os.getenv("MT5_PASSWORD", "")
MT5_SERVER = os.getenv("MT5_SERVER", "")

# Trading Parameters
SYMBOLS = ["AUDCAD", "AUDNZD", "EURCHF", "EURGBP", "USDCAD", "EURUSD", "USDCHF"]
TIMEFRAME_ENTRY = "M5"  
TIMEFRAME_HTF = "M15"
RISK_PER_TRADE_PERCENT = 1.0  # Risk 1% of account per trade
MAX_SPREAD_POINTS = 15

# ICT Parameters
FVG_MIN_SIZE_PIPS = 2.0
SWING_LOOKBACK = 5   # Number of candles to identify a swing high/low
