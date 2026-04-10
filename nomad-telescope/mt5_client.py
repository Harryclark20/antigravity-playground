import MetaTrader5 as mt5
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MT5Client:
    def __init__(self, login=None, password=None, server=None):
        self.login = str(login) if login else None
        self.password = str(password) if password else None
        self.server = str(server) if server else None
        self.connected = False

    def connect(self):
        logging.info("Initializing MT5...")
        if not mt5.initialize():
            logging.error(f"initialize() failed, error code = {mt5.last_error()}")
            return False
        
        if self.login and self.password and self.server:
            try:
                login_int = int(self.login)
                authorized = mt5.login(login_int, self.password, self.server)
                if not authorized:
                    logging.error(f"login() failed, error code: {mt5.last_error()}")
                    return False
            except ValueError:
                logging.error("Login must be an integer.")
                return False
                
        self.connected = True
        account_info = mt5.account_info()
        if account_info:
            logging.info(f"Connected. Balance: {account_info.balance} {account_info.currency}")
        return True

    def get_candles(self, symbol, timeframe, num_candles=100):
        if not self.connected:
            return pd.DataFrame()
            
        tf_map = {
            "M1": mt5.TIMEFRAME_M1,
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "H1": mt5.TIMEFRAME_H1
        }
        mt5_tf = tf_map.get(timeframe, mt5.TIMEFRAME_M1)
        
        rates = mt5.copy_rates_from_pos(symbol, mt5_tf, 0, num_candles)
        if rates is None or len(rates) == 0:
            return pd.DataFrame()
            
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df

    def get_tick(self, symbol):
        if not self.connected:
            return None
        return mt5.symbol_info_tick(symbol)

    def shutdown(self):
        mt5.shutdown()
        self.connected = False
        logging.info("MT5 connection closed.")
