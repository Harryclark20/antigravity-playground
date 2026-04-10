import requests
import logging
from typing import List, Dict

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataFetcher:
    def __init__(self):
        self.base_url = "https://api.dexscreener.com/latest/dex"

    def get_trending_tokens(self) -> List[Dict]:
        """
        Fetches the latest trending tokens. 
        Note: DexScreener doesn't have a direct 'trending' endpoint in the free tier,
        but we can search for recently created pairs or popular tokens.
        Alternatively, we might use the /tokens endpoint.
        For demonstrating logic, we will check Solana tokens.
        """
        try:
            # As a proxy for new trending memecoins, we specifically search for 'pump'
            # which isolates newly launched or highly volatile Pump.fun and Raydium coins.
            response = requests.get(f"{self.base_url}/search/?q=pump")
            response.raise_for_status()
            data = response.json()
            
            pairs = data.get('pairs', [])
            solana_pairs = [p for p in pairs if p.get('chainId') == 'solana']
            
            # Sort by 5-minute volume descending so it always checks the most explosive coins RIGHT NOW
            solana_pairs.sort(key=lambda x: x.get('volume', {}).get('m5', 0), reverse=True)
            
            return solana_pairs
        except Exception as e:
            logger.error(f"Error fetching trending tokens: {e}")
            return []

    def get_token_data(self, token_address: str) -> Dict:
        """
        Fetches specific data for a token address
        """
        try:
            response = requests.get(f"{self.base_url}/tokens/{token_address}")
            response.raise_for_status()
            data = response.json()
            
            pairs = data.get('pairs', [])
            if not pairs:
                return {}
            
            # Return the pair with the highest liquidity
            pairs.sort(key=lambda x: x.get('liquidity', {}).get('usd', 0), reverse=True)
            return pairs[0]
            
        except Exception as e:
            logger.error(f"Error fetching token data for {token_address}: {e}")
            return {}

    def fetch_historical_bars(self, pair_address: str):
        """
        Placeholder for fetching historical candlestick data.
        DexScreener API does not officially provide an OHLCV endpoint directly without authentication 
        or scraping. In a pro version, we'd use a service like Birdeye or paid DexScreener endpoints.
        For now, this is simulated or uses 24h/1h/5m change data provided in the normal pair response.
        """
        pass
