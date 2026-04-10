import MetaTrader5 as mt5
import json
import os

class MT5Gateway:
    def __init__(self, config_path='config.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
    def connect(self):
        """Initialize connection to MetaTrader 5 terminal."""
        if not mt5.initialize(
            path=self.config['mt5']['path'],
            login=self.config['mt5']['login'],
            password=self.config['mt5']['password'],
            server=self.config['mt5']['server']
        ):
            print(f"Failed to initialize MT5: {mt5.last_error()}")
            return False
        
        print(f"Successfully connected to MT5 Account: {self.config['mt5']['login']}")
        return True

    def get_account_info(self):
        """Returns account balance, equity, and leverage."""
        account_info = mt5.account_info()
        if account_info is None:
            return None
        return {
            "balance": account_info.balance,
            "equity": account_info.equity,
            "margin": account_info.margin,
            "margin_free": account_info.margin_free,
            "leverage": account_info.leverage
        }

    def shutdown(self):
        """Cleanly close the MT5 connection."""
        mt5.shutdown()
