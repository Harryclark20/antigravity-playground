import logging
import requests
import time
from typing import Dict
from config import PAPER_TRADE, PAYER_KEYPAIR, RPC_URL
from solana.rpc.api import Client
from solders.transaction import VersionedTransaction

logger = logging.getLogger(__name__)

class ExecutionEngine:
    def __init__(self):
        self.paper_trade = PAPER_TRADE
        self.open_positions: Dict[str, Dict] = {}
        self.paper_balance = 1000.0  # Start with 1000 USD for paper trading
        self.solana_client = Client(RPC_URL)
        
        # Wrapped SOL mint address on Solana
        self.WSOL_MINT = "So11111111111111111111111111111111111111112"
        self.BASE_TRADE_AMOUNT_SOL = 0.1 # Trade size per signal in real mode
        
        logger.info(f"Execution Engine Initialized. Paper Trade: {self.paper_trade}")

    def execute_Jupiter_swap(self, input_mint: str, output_mint: str, amount_lamports: int) -> bool:
        """ Uses Jupiter API v6 to quote and execute a swap """
        try:
            if not PAYER_KEYPAIR:
                logger.error("Real execution failed: No PAYER_KEYPAIR available.")
                return False

            # 1. Get Quote
            url = f"https://quote-api.jup.ag/v6/quote?inputMint={input_mint}&outputMint={output_mint}&amount={amount_lamports}&slippageBps=50"
            quote_res = requests.get(url)
            quote_res.raise_for_status()
            quote_response = quote_res.json()
            
            # 2. Get Transaction
            swap_res = requests.post(
                "https://quote-api.jup.ag/v6/swap",
                json={
                    "quoteResponse": quote_response,
                    "userPublicKey": str(PAYER_KEYPAIR.pubkey()),
                    "wrapAndUnwrapSol": True,
                }
            )
            swap_res.raise_for_status()
            swap_info = swap_res.json()
            swap_transaction_buf = bytes.fromhex(swap_info['swapTransaction'])
            
            # 3. Deserialize and Sign
            transaction = VersionedTransaction.from_bytes(swap_transaction_buf)
            signature = PAYER_KEYPAIR.sign_message(transaction.message.to_bytes_versioned())
            signed_tx = VersionedTransaction.populate(transaction.message, [signature])
            
            # 4. Broadcast
            send_res = self.solana_client.send_raw_transaction(bytes(signed_tx))
            logger.info(f"[REAL TRADE SENT] Transaction Signature: {send_res.value}")
            return True
            
        except Exception as e:
            logger.error(f"Jupiter Swap Error: {str(e)}")
            return False

    def execute_buy(self, token_address: str, pair_data: Dict, amount_usd: float = 50.0) -> bool:
        token_symbol = pair_data.get('baseToken', {}).get('symbol', 'UNKNOWN')
        current_price = float(pair_data.get('priceUsd', 0))
        
        if current_price <= 0:
            return False

        if self.paper_trade:
            if amount_usd > self.paper_balance:
                return False
                
            token_amount = amount_usd / current_price
            self.paper_balance -= amount_usd
            self.open_positions[token_address] = {
                'symbol': token_symbol,
                'buy_price': current_price,
                'amount_tokens': token_amount,
                'amount_usd': amount_usd
            }
            logger.info(f"[PAPER BOUGHT] {token_symbol} at ${current_price}. Balance: ${self.paper_balance:.2f}")
            return True
        else:
            logger.info(f"[LIVE BUY] Attempting to buy {token_symbol} via Jupiter...")
            # Example: Trading 0.1 SOL for the Token. (1 SOL = 1,000,000,000 Lamports)
            amount_lamports = int(self.BASE_TRADE_AMOUNT_SOL * 1_000_000_000)
            
            success = self.execute_Jupiter_swap(self.WSOL_MINT, token_address, amount_lamports)
            if success:
                # In a robust system, you'd wait for confirmation here, 
                # but for simplicity we log the open position instantly.
                token_amount = (self.BASE_TRADE_AMOUNT_SOL * float(pair_data.get('priceNative', 0))) # approximation
                self.open_positions[token_address] = {
                    'symbol': token_symbol,
                    'buy_price': current_price,
                    'amount_tokens': token_amount,
                    'amount_usd': amount_usd # approximate
                }
            return success

    def execute_sell(self, token_address: str, current_price: float, reason: str = "") -> bool:
        if token_address not in self.open_positions:
            return False
            
        position = self.open_positions[token_address]
        token_symbol = position['symbol']
        tokens = position['amount_tokens']

        if self.paper_trade:
            revenue = tokens * current_price
            profit = revenue - position['amount_usd']
            self.paper_balance += revenue
            
            logger.info(f"[PAPER SOLD] {token_symbol} at ${current_price}. Reason: {reason}. Profit: ${profit:.2f}. Balance: ${self.paper_balance:.2f}")
            del self.open_positions[token_address]
            return True
        else:
            logger.info(f"[LIVE SELL] Attempting to sell {token_symbol} via Jupiter... Reason: {reason}")
            # Get token decimals to calculate lamports. For simplicity, assume 6 decimals or fetch it via RPC.
            # Using 6 as a common default for memecoins, but could fail if it's 9.
            # A completely robust bot MUST fetch the token decimals via `get_token_supply`.
            token_lamports = int(tokens * 1_000_000) 
            
            success = self.execute_Jupiter_swap(token_address, self.WSOL_MINT, token_lamports)
            if success:
                del self.open_positions[token_address]
            return success
