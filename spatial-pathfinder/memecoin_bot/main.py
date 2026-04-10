import time
import logging
from config import RPC_URL, CHECK_INTERVAL_SECONDS
from data_fetcher import DataFetcher
from security_checker import SecurityChecker
from strategy import TradingStrategy
from execution import ExecutionEngine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Memecoin Trading Bot...")

    # Initialize components
    fetcher = DataFetcher()
    security = SecurityChecker(rpc_url=RPC_URL)
    strategy = TradingStrategy()
    executor = ExecutionEngine()

    while True:
        try:
            logger.info("--- New Cycle ---")
            
            # 1. Evaluate Open Positions (Exit Strategy)
            for token_address in list(executor.open_positions.keys()):
                # Fetch fresh data for the open position
                pair_data = fetcher.get_token_data(token_address)
                if not pair_data:
                    continue
                    
                current_price = float(pair_data.get('priceUsd', 0))
                buy_price = executor.open_positions[token_address]['buy_price']
                
                # Check for exit signals
                should_exit, reason = strategy.evaluate_exit(buy_price, current_price)
                if should_exit:
                    executor.execute_sell(token_address, current_price, reason)
                else:
                    logger.info(f"Holding {executor.open_positions[token_address]['symbol']}: {reason}")
            
            # 2. Find New Opportunities (Entry Strategy)
            if len(executor.open_positions) < 3: # Max 3 concurrent positions
                trending_pairs = fetcher.get_trending_tokens()
                
                for pair in trending_pairs[:10]: # Check top 10
                    token_address = pair.get('baseToken', {}).get('address', '')
                    
                    if token_address in executor.open_positions:
                        continue # Already holding
                        
                    # Check Security
                    if not security.check_token_safety(token_address, pair):
                        continue
                        
                    # Evaluate Strategy
                    if strategy.evaluate_entry(pair):
                        logger.info(f"Signal confirmed for {pair.get('baseToken', {}).get('symbol')}, executing buy...")
                        # Execute Buy (Risking $50 per trade paper)
                        executor.execute_buy(token_address, pair, amount_usd=50.0)
                        break # Only buy one token per cycle to manage rate limits
                        
            time.sleep(CHECK_INTERVAL_SECONDS)
            
        except KeyboardInterrupt:
            logger.info("Bot stopped by user.")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
