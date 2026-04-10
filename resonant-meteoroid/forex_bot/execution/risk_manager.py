import MetaTrader5 as mt5
import logging
from datetime import datetime, time

logger = logging.getLogger(__name__)

class RiskManager:
    def __init__(self, max_daily_loss_percent=3.0, max_trades_per_day=10, max_consecutive_losses=3):
        self.max_daily_loss_percent = max_daily_loss_percent
        self.max_trades_per_day = max_trades_per_day
        self.max_consecutive_losses = max_consecutive_losses
        
        self.daily_start_balance = 0.0
        self.current_date = None
        self.trades_today = 0
        self.consecutive_losses = 0
        self.trading_halted = False

    def _update_daily_stats(self):
        """Reset daily statistics at the start of a new trading day."""
        now = datetime.now()
        if self.current_date != now.date():
            self.current_date = now.date()
            self.trades_today = 0
            self.consecutive_losses = 0
            self.trading_halted = False
            
            account_info = mt5.account_info()
            if account_info:
                self.daily_start_balance = account_info.balance
            logger.info(f"New trading day started. Starting balance: {self.daily_start_balance}")

    def update_after_trade(self, profit: float):
        """Update consecutive losses after a trade closes."""
        if profit < 0:
            self.consecutive_losses += 1
            logger.info(f"Trade closed in loss. Consecutive losses: {self.consecutive_losses}")
        else:
            self.consecutive_losses = 0
            logger.info("Trade closed in profit. Reset consecutive losses.")

    def can_trade(self) -> bool:
        """Evaluate if trading is currently allowed based on risk rules."""
        self._update_daily_stats()

        if self.trading_halted:
            return False

        account_info = mt5.account_info()
        if not account_info:
            logger.warning("Could not retrieve account info for risk check.")
            return False

        # Check max trades
        # While trades_today tracks initiated trades locally, MT5 history gives the full picture
        # We assume local tracking + history check if needed. For now, local tracking.
        if self.trades_today >= self.max_trades_per_day:
            logger.warning(f"Max trades per day ({self.max_trades_per_day}) reached. Halting trading.")
            self.trading_halted = True
            return False

        # Check consecutive losses
        if self.consecutive_losses >= self.max_consecutive_losses:
            logger.warning(f"Max consecutive losses ({self.max_consecutive_losses}) reached. Halting trading.")
            self.trading_halted = True
            return False

        # Check daily loss limit
        current_equity = account_info.equity
        if self.daily_start_balance > 0:
            loss = self.daily_start_balance - current_equity
            loss_percent = (loss / self.daily_start_balance) * 100
            
            if loss_percent >= self.max_daily_loss_percent:
                logger.warning(f"Daily loss limit reached ({loss_percent:.2f}% >= {self.max_daily_loss_percent}%). Halting.")
                self.trading_halted = True
                return False

        return True

    def record_trade_start(self):
        self.trades_today += 1
