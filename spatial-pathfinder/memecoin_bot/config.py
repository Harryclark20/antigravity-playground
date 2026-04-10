import os
from dotenv import load_dotenv

load_dotenv()

# Network Configuration
NETWORK = "mainnet" # Using mainnet for data, paper trading for execution
RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")

# Bot State
PAPER_TRADE = os.getenv("PAPER_TRADE", "True").lower() in ("true", "1", "yes")

# Wallet (for later real execution)
from solders.keypair import Keypair

PRIVATE_KEY_STR = os.getenv("PRIVATE_KEY", "")
PAYER_KEYPAIR = None
if not PAPER_TRADE and PRIVATE_KEY_STR:
    try:
        PAYER_KEYPAIR = Keypair.from_base58_string(PRIVATE_KEY_STR)
    except Exception as e:
        print(f"Failed to load Private Key: {e}")


# --- Trading Strategy Parameters ---
# Trend/Momentum
VOLUME_SPIKE_MULTIPLIER = 2.5  # Volume must be X times the moving average
MIN_LIQUIDITY_USD = 10000      # Minimum amount of liquidity in the pool
MAX_MCAP_USD = 10000000        # Ignore high market cap established coins

# Exit Strategy
STOP_LOSS_PCT = 0.15           # 15% stop loss
TAKE_PROFIT_PCT = 0.50         # 50% take profit
TRAILING_STOP_BPS = 500        # 5% trailing stop-loss

# Cycle Check timing
CHECK_INTERVAL_SECONDS = 10
