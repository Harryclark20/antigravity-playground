import MetaTrader5 as mt5
import json
import os

class MT5Gateway:
    def __init__(self, config_path='config.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
    def connect(self):
        """Initialize connection to MetaTrader 5 terminal."""
        # If login is 0 or YOUR_PASSWORD placeholder is present, try parameterless init
        if self.config['mt5']['login'] == 0 or self.config['mt5']['password'] == "YOUR_PASSWORD":
            print("No credentials provided. Attempting to connect to active MT5 session...")
            if not mt5.initialize():
                print(f"Failed to initialize MT5: {mt5.last_error()}")
                return False
        else:
            if not mt5.initialize(
                path=self.config['mt5']['path'],
                login=self.config['mt5']['login'],
                password=self.config['mt5']['password'],
                server=self.config['mt5']['server']
            ):
                print(f"Failed to initialize MT5: {mt5.last_error()}")
                return False
        
        account_info = mt5.account_info()
        if account_info:
            print(f"Successfully connected to MT5 Account: {account_info.login}")
        else:
            print("Connected to MT5, but could not retrieve account info.")
            
        return True

    def get_account_info(self):
        """Returns account balance, equity, and leverage."""
        account_info = mt5.account_info()
        if account_info is None:
            return None
        return {
            "login": account_info.login,
            "server": account_info.server,
            "name": account_info.name,
            "currency": account_info.currency,
            "balance": account_info.balance,
            "equity": account_info.equity,
            "margin": account_info.margin,
            "margin_free": account_info.margin_free,
            "leverage": account_info.leverage
        }

    def get_ticks(self, symbol, datetime_from, count, flags=mt5.COPY_TICKS_ALL):
        """Retrieve recent tick data for a specific symbol."""
        ticks = mt5.copy_ticks_from(symbol, datetime_from, count, flags)
        return ticks

    def get_symbol_info(self, symbol):
        """Returns detailed symbol information (spread, point, etc)."""
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            return None
        return {
            "bid": symbol_info.bid,
            "ask": symbol_info.ask,
            "spread": symbol_info.spread,
            "digits": symbol_info.digits,
            "point": symbol_info.point
        }

    def get_server_time(self, symbol="EURUSD"):
        """
        Returns a local datetime anchored to the broker's server clock.
        This is the correct way to handle MT5 tick fetching regardless of
        local timezone offsets — MT5 copy_ticks_from() expects a local datetime
        that corresponds to the server's current time.
        """
        import datetime
        tick = mt5.symbol_info_tick(symbol)
        if tick:
            return datetime.datetime.fromtimestamp(tick.time)
        return datetime.datetime.now()

    def shutdown(self):
        """Cleanly close the MT5 connection."""
        mt5.shutdown()
