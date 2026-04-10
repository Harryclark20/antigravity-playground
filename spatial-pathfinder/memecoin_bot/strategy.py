import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

class TradingStrategy:
    def __init__(self):
        pass

    def evaluate_entry(self, pair_data: Dict) -> bool:
        """
        Evaluates whether a token meets the criteria to buy.
        Criteria:
        1. Trending up in the very short term (e.g. 5m or 1h).
        2. High volume indicating momentum.
        """
        token_name = pair_data.get('baseToken', {}).get('symbol', 'UNKNOWN')
        
        price_change = pair_data.get('priceChange', {})
        h1_change = price_change.get('h1', 0)
        m5_change = price_change.get('m5', 0)
        
        if m5_change > 2.0 and h1_change > 5.0:
            logger.info(f"ENTRY SIGNAL for {token_name}: +{m5_change}%(5m) +{h1_change}%(1h)")
            return True
            
        logger.info(f"Skipping {token_name}: Momentum too low. (5m: +{m5_change}%, 1h: +{h1_change}%)")
        return False
        
    def evaluate_exit(self, buy_price: float, current_price: float) -> Tuple[bool, str]:
        """
        Returns (ShouldExit, Reason)
        Uses Stop Loss and Take Profit parameters from config.
        """
        from config import STOP_LOSS_PCT, TAKE_PROFIT_PCT
        
        if buy_price <= 0:
            return False, ""
            
        pnl_pct = (current_price - buy_price) / buy_price
        
        # Stop Loss hit
        if pnl_pct <= -STOP_LOSS_PCT:
            return True, f"Stop Loss Triggered ({pnl_pct*100:.2f}%)"
            
        # Take Profit hit
        if pnl_pct >= TAKE_PROFIT_PCT:
            return True, f"Take Profit Triggered ({pnl_pct*100:.2f}%)"
            
        # Could also implement trend reversal exits (e.g., m5_change < -5%) by passing more data.
        return False, f"Holding. PnL: {pnl_pct*100:.2f}%"
